import os
import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from .models import Document, DocumentChunk, KnowledgeBase
from .vectorstore import count_vectors


User = get_user_model()


class KnowledgeBaseApiTests(APITestCase):
    # 覆盖鉴权、创建索引文件、用户隔离与删除清理
    def setUp(self):
        self.user1 = User.objects.create_user(username="kb_u1", password="StrongPass123!@#")
        self.user2 = User.objects.create_user(username="kb_u2", password="StrongPass123!@#")

    def _login_and_get_access(self, username: str, password: str) -> str:
        resp = self.client.post(
            "/api/users/login",
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        return resp.data["access"]

    def test_auth_required(self):
        self.assertEqual(self.client.post("/api/kb/create", {"name": "kb1"}, format="json").status_code, 401)
        self.assertEqual(self.client.get("/api/kb/list").status_code, 401)
        self.assertEqual(self.client.delete("/api/kb/999").status_code, 401)

    def test_create_list_delete_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(FAISS_INDEX_ROOT=Path(tmpdir)):
                access1 = self._login_and_get_access("kb_u1", "StrongPass123!@#")

                create_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1", "description": "d1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(create_resp.status_code, 201)
                kb_id = create_resp.data["id"]
                faiss_path = create_resp.data["faiss_path"]
                self.assertTrue(Path(faiss_path).is_file())
                self.assertTrue(KnowledgeBase.objects.filter(id=kb_id, user=self.user1).exists())

                KnowledgeBase.objects.create(
                    user=self.user2,
                    name="kb_other",
                    description="",
                    faiss_path=str(Path(tmpdir) / "user_2" / "kb_999.index"),
                )

                list_resp = self.client.get(
                    "/api/kb/list",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(list_resp.status_code, 200)
                ids = [item["id"] for item in list_resp.data["items"]]
                self.assertIn(kb_id, ids)
                self.assertNotIn("kb_other", [item["name"] for item in list_resp.data["items"]])

                del_resp = self.client.delete(
                    f"/api/kb/{kb_id}",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(del_resp.status_code, 204)
                self.assertFalse(KnowledgeBase.objects.filter(id=kb_id).exists())
                self.assertFalse(Path(faiss_path).exists())

    def test_delete_ignores_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(FAISS_INDEX_ROOT=Path(tmpdir)):
                access1 = self._login_and_get_access("kb_u1", "StrongPass123!@#")

                create_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(create_resp.status_code, 201)
                kb_id = create_resp.data["id"]
                faiss_path = Path(create_resp.data["faiss_path"])
                faiss_path.unlink(missing_ok=True)

                del_resp = self.client.delete(
                    f"/api/kb/{kb_id}",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(del_resp.status_code, 204)

    def test_cannot_delete_others_kb(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(FAISS_INDEX_ROOT=Path(tmpdir)):
                access1 = self._login_and_get_access("kb_u1", "StrongPass123!@#")
                access2 = self._login_and_get_access("kb_u2", "StrongPass123!@#")

                create_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access2}",
                )
                kb_id = create_resp.data["id"]

                del_resp = self.client.delete(
                    f"/api/kb/{kb_id}",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(del_resp.status_code, 404)


class DocumentIngestionApiTests(APITestCase):
    def setUp(self):
        os.environ["KB_EMBEDDING_BACKEND"] = "fake"
        self.user1 = User.objects.create_user(username="doc_u1", password="StrongPass123!@#")
        self.user2 = User.objects.create_user(username="doc_u2", password="StrongPass123!@#")

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

    def test_upload_list_delete_flow(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                access1 = self._login_and_get_access("doc_u1", "StrongPass123!@#")

                kb_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(kb_resp.status_code, 201)
                kb_id = kb_resp.data["id"]
                kb_faiss_path = Path(kb_resp.data["faiss_path"])

                upload_file = SimpleUploadedFile("a.txt", b"hello world\n" * 50, content_type="text/plain")
                up_resp = self.client.post(
                    "/api/kb/upload",
                    {"kb_id": kb_id, "file": upload_file},
                    format="multipart",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(up_resp.status_code, 201)
                doc_id = up_resp.data["id"]
                self.assertTrue(Document.objects.filter(id=doc_id, kb_id=kb_id).exists())
                self.assertGreater(DocumentChunk.objects.filter(document_id=doc_id).count(), 0)

                doc = Document.objects.get(id=doc_id)
                self.assertTrue(Path(doc.file_path).is_file())
                self.assertGreater(count_vectors(kb_faiss_path), 0)

                list_resp = self.client.get(
                    f"/api/kb/{kb_id}/documents",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(list_resp.status_code, 200)
                self.assertEqual(len(list_resp.data["items"]), 1)
                self.assertEqual(list_resp.data["items"][0]["id"], doc_id)

                del_resp = self.client.delete(
                    f"/api/document/{doc_id}",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(del_resp.status_code, 204)
                self.assertFalse(Document.objects.filter(id=doc_id).exists())
                self.assertEqual(DocumentChunk.objects.filter(document_id=doc_id).count(), 0)
                self.assertEqual(count_vectors(kb_faiss_path), 0)

    def test_auth_and_ownership(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                access1 = self._login_and_get_access("doc_u1", "StrongPass123!@#")
                access2 = self._login_and_get_access("doc_u2", "StrongPass123!@#")

                kb_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                kb_id = kb_resp.data["id"]

                self.assertEqual(
                    self.client.post(
                        "/api/kb/upload",
                        {"kb_id": kb_id, "file": SimpleUploadedFile("a.txt", b"t")},
                        format="multipart",
                    ).status_code,
                    401,
                )
                self.assertEqual(self.client.get(f"/api/kb/{kb_id}/documents").status_code, 401)

                other_list_resp = self.client.get(
                    f"/api/kb/{kb_id}/documents",
                    HTTP_AUTHORIZATION=f"Bearer {access2}",
                )
                self.assertEqual(other_list_resp.status_code, 404)

    def test_upload_duplicate_keep(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                access1 = self._login_and_get_access("doc_u1", "StrongPass123!@#")

                kb_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                kb_id = kb_resp.data["id"]
                kb_faiss_path = Path(kb_resp.data["faiss_path"])

                f1 = SimpleUploadedFile("a.txt", b"x" * 5000, content_type="text/plain")
                r1 = self.client.post(
                    "/api/kb/upload",
                    {"kb_id": kb_id, "file": f1, "on_conflict": "keep"},
                    format="multipart",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(r1.status_code, 201)
                self.assertEqual(r1.data["filename"], "a.txt")

                before = count_vectors(kb_faiss_path)

                f2 = SimpleUploadedFile("a.txt", b"y" * 5000, content_type="text/plain")
                r2 = self.client.post(
                    "/api/kb/upload",
                    {"kb_id": kb_id, "file": f2, "on_conflict": "keep"},
                    format="multipart",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(r2.status_code, 201)
                self.assertNotEqual(r2.data["filename"], "a.txt")
                self.assertTrue(r2.data["filename"].endswith(".txt"))

                self.assertEqual(Document.objects.filter(kb_id=kb_id).count(), 2)
                self.assertGreater(count_vectors(kb_faiss_path), before)

    def test_upload_duplicate_replace(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                access1 = self._login_and_get_access("doc_u1", "StrongPass123!@#")

                kb_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                kb_id = kb_resp.data["id"]
                kb_faiss_path = Path(kb_resp.data["faiss_path"])

                f1 = SimpleUploadedFile("a.txt", b"x" * 5000, content_type="text/plain")
                r1 = self.client.post(
                    "/api/kb/upload",
                    {"kb_id": kb_id, "file": f1, "on_conflict": "keep"},
                    format="multipart",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(r1.status_code, 201)

                f2 = SimpleUploadedFile("a.txt", b"z" * 3000, content_type="text/plain")
                r2 = self.client.post(
                    "/api/kb/upload",
                    {"kb_id": kb_id, "file": f2, "on_conflict": "replace"},
                    format="multipart",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(r2.status_code, 201)
                self.assertEqual(r2.data["filename"], "a.txt")

                self.assertEqual(Document.objects.filter(kb_id=kb_id, filename="a.txt").count(), 1)
                total_chunks = DocumentChunk.objects.filter(document__kb_id=kb_id).count()
                self.assertEqual(count_vectors(kb_faiss_path), total_chunks)
