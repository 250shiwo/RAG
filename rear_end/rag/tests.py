import os
import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APITestCase


User = get_user_model()


class RagChatApiTests(APITestCase):
    def setUp(self):
        os.environ["KB_EMBEDDING_BACKEND"] = "fake"
        os.environ["RAG_LLM_BACKEND"] = "fake"
        self.user1 = User.objects.create_user(username="rag_u1", password="StrongPass123!@#")
        self.user2 = User.objects.create_user(username="rag_u2", password="StrongPass123!@#")

    def tearDown(self):
        os.environ.pop("KB_EMBEDDING_BACKEND", None)
        os.environ.pop("RAG_LLM_BACKEND", None)

    def _login_and_get_access(self, username: str, password: str) -> str:
        resp = self.client.post(
            "/api/users/login",
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        return resp.data["access"]

    def test_auth_required(self):
        resp = self.client.post("/api/rag/chat", {"kb_id": 1, "question": "hi"}, format="json")
        self.assertEqual(resp.status_code, 401)

    def test_invalid_input(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                access1 = self._login_and_get_access("rag_u1", "StrongPass123!@#")

                kb_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(kb_resp.status_code, 201)
                kb_id = kb_resp.data["id"]

                r1 = self.client.post(
                    "/api/rag/chat",
                    {"kb_id": kb_id, "question": ""},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(r1.status_code, 400)

                r2 = self.client.post(
                    "/api/rag/chat",
                    {"question": "hi"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(r2.status_code, 400)

    def test_cannot_chat_others_kb(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                access1 = self._login_and_get_access("rag_u1", "StrongPass123!@#")
                access2 = self._login_and_get_access("rag_u2", "StrongPass123!@#")

                kb_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(kb_resp.status_code, 201)
                kb_id = kb_resp.data["id"]

                r = self.client.post(
                    "/api/rag/chat",
                    {"kb_id": kb_id, "question": "hi"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access2}",
                )
                self.assertEqual(r.status_code, 404)

    def test_chat_returns_answer(self):
        with tempfile.TemporaryDirectory() as faiss_dir, tempfile.TemporaryDirectory() as upload_dir:
            with override_settings(FAISS_INDEX_ROOT=Path(faiss_dir), KB_UPLOAD_ROOT=Path(upload_dir)):
                access1 = self._login_and_get_access("rag_u1", "StrongPass123!@#")

                kb_resp = self.client.post(
                    "/api/kb/create",
                    {"name": "kb1"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(kb_resp.status_code, 201)
                kb_id = kb_resp.data["id"]

                upload_file = SimpleUploadedFile("a.txt", b"hello rag\n" * 50, content_type="text/plain")
                up_resp = self.client.post(
                    "/api/kb/upload",
                    {"kb_id": kb_id, "file": upload_file},
                    format="multipart",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(up_resp.status_code, 201)

                chat_resp = self.client.post(
                    "/api/rag/chat",
                    {"kb_id": kb_id, "question": "hello?"},
                    format="json",
                    HTTP_AUTHORIZATION=f"Bearer {access1}",
                )
                self.assertEqual(chat_resp.status_code, 200)
                self.assertTrue(isinstance(chat_resp.data.get("answer"), str))
                self.assertTrue(chat_resp.data["answer"].strip())
                self.assertTrue(isinstance(chat_resp.data.get("elapsed_ms"), int))
                self.assertGreaterEqual(chat_resp.data["elapsed_ms"], 0)
                self.assertTrue(isinstance(chat_resp.data.get("token_usage"), dict))
                self.assertIn("prompt_tokens", chat_resp.data["token_usage"])
                self.assertIn("completion_tokens", chat_resp.data["token_usage"])
                self.assertIn("total_tokens", chat_resp.data["token_usage"])
