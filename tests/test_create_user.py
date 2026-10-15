import allure
import pytest

from data.errors import REQUIRED_FIELDS_MISSING, USER_ALREADY_EXISTS
from data.user_data import REQUIRED_REGISTRATION_FIELDS, generate_unique_user


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.story("Создание уникального пользователя")
    def test_create_unique_user_success(self, user_api, cleanup_user):
        payload = generate_unique_user()
        response = user_api.register(payload)

        cleanup_user(response.json()["accessToken"])

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == payload["email"]
        assert body["user"]["name"] == payload["name"]

    @allure.story("Создание пользователя с существующим email")
    def test_create_user_with_existing_email_error(self, user_api, created_user):
        duplicate = {
            "email": created_user["email"],
            "password": "anotherPassword",
            "name": "Another Name",
        }
        response = user_api.register(duplicate)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == USER_ALREADY_EXISTS
        assert "accessToken" not in body
        assert "user" not in body

    @allure.story("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", REQUIRED_REGISTRATION_FIELDS)
    def test_create_user_without_required_field_error(self, user_api, missing_field):
        payload = generate_unique_user()
        del payload[missing_field]

        response = user_api.register(payload)

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == REQUIRED_FIELDS_MISSING
        assert "accessToken" not in body
        assert "user" not in body
        