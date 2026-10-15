import allure
import pytest

from data.errors import AUTH_REQUIRED, USER_EMAIL_ALREADY_EXISTS
from data.user_data import (
    NEW_PASSWORD,
    UPDATABLE_USER_FIELDS_IN_RESPONSE,
)


@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.story("Изменение email с авторизацией")
    @pytest.mark.parametrize("field,new_value", UPDATABLE_USER_FIELDS_IN_RESPONSE)
    def test_update_user_with_auth_success(
        self, user_api, created_user, field, new_value
    ):
        response = user_api.update(
            {field: new_value}, token=created_user["token"]
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"][field] == new_value

    @allure.story("Изменение пароля с авторизацией")
    def test_update_user_password_with_auth_success(self, user_api, created_user):
        response = user_api.update(
            {"password": NEW_PASSWORD}, token=created_user["token"]
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "password" not in body["user"]

        # Проверяем, что новый пароль действительно работает
        login_response = user_api.login({
            "email": created_user["email"],
            "password": NEW_PASSWORD,
        })
        assert login_response.status_code == 200
        assert login_response.json()["success"] is True

    @allure.story("Изменение данных без авторизации")
    @pytest.mark.parametrize("field,new_value", UPDATABLE_USER_FIELDS_IN_RESPONSE)
    def test_update_user_without_auth_error(
        self, user_api, created_user, field, new_value
    ):
        response = user_api.update_without_token({field: new_value})

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == AUTH_REQUIRED
        assert "user" not in body

    @allure.story("Изменение email на уже занятый")
    def test_update_user_with_existing_email_error(
        self, user_api, created_user, second_user
    ):
        response = user_api.update(
            {"email": second_user["email"]},
            token=created_user["token"],
        )

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == USER_EMAIL_ALREADY_EXISTS
        assert "user" not in body