import os
import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase


User = get_user_model()


class AdminApiTests(APITestCase):
    def setUp(self):
        os.environ["KB_EMBEDDING_BACKEND"] = "fake"
        self.admin = User.objects.create_user(username="admin_u1", password="StrongPass123!@#")
        self.admin.is_staff = True
        self.admin.save(update_fields=["is_staff"])
        self.user = User.objects.create_user(username="normal_u1", password="StrongPass123!@#")

    def tearDown(self):
        os.environ.pop("KB_EMBEDDING_BACKEND", None)

    def _login_and_get_access(self, username: str, password: str) -> str:
        resp = self.client.post(
            "/api/users/login",
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        return resp.data["access"]

    def test_admin_endpoints_require_admin(self):
        r1 = self.client.get("/api/admin/users")
        self.assertEqual(r1.status_code, 401)

        access = self._login_and_get_access("normal_u1", "StrongPass123!@#")
        r2 = self.client.get("/api/admin/users", HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(r2.status_code, 403)

    def test_admin_user_crud(self):
        access = self._login_and_get_access("admin_u1", "StrongPass123!@#")

        created = self.client.post(
            "/api/admin/users",
            {"username": "u2", "password": "StrongPass123!@#", "email": "a@b.com", "is_active": True},
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(created.status_code, 201)
        user_id = created.data["id"]

        lst = self.client.get("/api/admin/users?q=u2", HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(lst.status_code, 200)
        self.assertTrue(any(x["id"] == user_id for x in lst.data.get("items", [])))

        patched = self.client.patch(
            f"/api/admin/users/{user_id}",
            {"email": "c@d.com", "is_active": False},
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(patched.status_code, 200)
        self.assertEqual(patched.data["email"], "c@d.com")
        self.assertEqual(patched.data["is_active"], False)

        deleted = self.client.delete(f"/api/admin/users/{user_id}", HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(deleted.status_code, 204)

        deleted_again = self.client.delete(f"/api/admin/users/{user_id}", HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(deleted_again.status_code, 404)

    def test_admin_kb_and_document_flow(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                admin_access = self._login_and_get_access("admin_u1", "StrongPass123!@#")

                kb_created = self.client.post(
                    "/api/admin/kb",
                    {"user_id": self.user.id, "name": "kb1", "description": "d1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {admin_access}",
                )
                self.assertEqual(kb_created.status_code, 201)
                kb_id = kb_created.data["id"]
                self.assertEqual(kb_created.data["user_id"], self.user.id)

                self.assertTrue(Path(kb_created.data["faiss_path"]).exists())

                user_access = self._login_and_get_access("normal_u1", "StrongPass123!@#")
                upload_file = SimpleUploadedFile("a.txt", b"hello admin\n" * 50, content_type="text/plain")
                up_resp = self.client.post(
                    "/api/kb/upload",
                    {"kb_id": kb_id, "file": upload_file},
                    format="multipart",
                    HTTP_AUTHORIZATION=f"Bearer {user_access}",
                )
                self.assertEqual(up_resp.status_code, 201)
                doc_id = up_resp.data["id"]

                docs = self.client.get(
                    f"/api/admin/kb/{kb_id}/documents",
                    HTTP_AUTHORIZATION=f"Bearer {admin_access}",
                )
                self.assertEqual(docs.status_code, 200)
                self.assertTrue(any(x["id"] == doc_id for x in docs.data.get("items", [])))

                del_doc = self.client.delete(
                    f"/api/admin/document/{doc_id}",
                    HTTP_AUTHORIZATION=f"Bearer {admin_access}",
                )
                self.assertEqual(del_doc.status_code, 204)

                docs2 = self.client.get(
                    f"/api/admin/kb/{kb_id}/documents",
                    HTTP_AUTHORIZATION=f"Bearer {admin_access}",
                )
                self.assertEqual(docs2.status_code, 200)
                self.assertFalse(any(x["id"] == doc_id for x in docs2.data.get("items", [])))

                del_kb = self.client.delete(f"/api/admin/kb/{kb_id}", HTTP_AUTHORIZATION=f"Bearer {admin_access}")
                self.assertEqual(del_kb.status_code, 204)
                self.assertFalse(Path(kb_created.data["faiss_path"]).exists())

