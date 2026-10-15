import allure

from data.errors import INCORRECT_CREDENTIALS
from data.user_data import WRONG_EMAIL, WRONG_PASSWORD


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.story("Логин под существующим пользователем")
    def test_login_with_valid_credentials_success(self, user_api, created_user):
        response = user_api.login({
            "email": created_user["email"],
            "password": created_user["password"],
        })

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == created_user["email"]

    @allure.story("Логин с неверным email")
    def test_login_with_wrong_email_error(self, user_api, created_user):
        response = user_api.login({
            "email": WRONG_EMAIL,
            "password": created_user["password"],
        })

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == INCORRECT_CREDENTIALS
        assert "accessToken" not in body
        assert "user" not in body

    @allure.story("Логин с неверным паролем")
    def test_login_with_wrong_password_error(self, user_api, created_user):
        response = user_api.login({
            "email": created_user["email"],
            "password": WRONG_PASSWORD,
        })

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == INCORRECT_CREDENTIALS
        assert "accessToken" not in body
        assert "user" not in body

    @allure.story("Логин с неверным email и паролем")
    def test_login_with_wrong_email_and_password_error(self, user_api, created_user):
        response = user_api.login({
            "email": WRONG_EMAIL,
            "password": WRONG_PASSWORD,
        })

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == INCORRECT_CREDENTIALS
        assert "accessToken" not in body
        assert "user" not in body
        