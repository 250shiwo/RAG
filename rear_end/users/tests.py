from rest_framework.test import APITestCase


class UserAuthApiTests(APITestCase):
    # 这里用接口串联验证：注册 -> 登录 -> me（鉴权）
    def test_register_login_me_flow(self):
        register_resp = self.client.post(
            "/api/users/register",
            {"username": "u1", "password": "StrongPass123!@#"},
            format="json",
        )
        self.assertEqual(register_resp.status_code, 201)
        self.assertIn("id", register_resp.data)
        self.assertEqual(register_resp.data["username"], "u1")
        self.assertNotIn("password", register_resp.data)

        duplicate_resp = self.client.post(
            "/api/users/register",
            {"username": "u1", "password": "StrongPass123!@#"},
            format="json",
        )
        self.assertEqual(duplicate_resp.status_code, 400)

        login_resp = self.client.post(
            "/api/users/login",
            {"username": "u1", "password": "StrongPass123!@#"},
            format="json",
        )
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("access", login_resp.data)
        self.assertIn("refresh", login_resp.data)

        refresh_resp = self.client.post(
            "/api/users/refresh",
            {"refresh": login_resp.data["refresh"]},
            format="json",
        )
        self.assertEqual(refresh_resp.status_code, 200)
        self.assertIn("access", refresh_resp.data)

        bad_login_resp = self.client.post(
            "/api/users/login",
            {"username": "u1", "password": "wrong-password"},
            format="json",
        )
        self.assertEqual(bad_login_resp.status_code, 401)

        me_unauth_resp = self.client.get("/api/users/me")
        self.assertEqual(me_unauth_resp.status_code, 401)

        access = login_resp.data["access"]
        me_auth_resp = self.client.get(
            "/api/users/me",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(me_auth_resp.status_code, 200)
        self.assertEqual(me_auth_resp.data["username"], "u1")

        refreshed_access = refresh_resp.data["access"]
        me_auth_refreshed_resp = self.client.get(
            "/api/users/me",
            HTTP_AUTHORIZATION=f"Bearer {refreshed_access}",
        )
        self.assertEqual(me_auth_refreshed_resp.status_code, 200)
        self.assertEqual(me_auth_refreshed_resp.data["username"], "u1")
