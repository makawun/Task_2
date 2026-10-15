import allure

from data.errors import AUTH_REQUIRED, INGREDIENTS_REQUIRED
from data.order_data import DEFAULT_INGREDIENTS_COUNT, INVALID_INGREDIENT_HASHES


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(
        self, order_api, created_user, available_ingredient_ids
    ):
        payload = {"ingredients": available_ingredient_ids[:DEFAULT_INGREDIENTS_COUNT]}
        response = order_api.create(payload, token=created_user["token"])

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "name" in body
        assert "order" in body
        assert body["order"]["number"] is not None

    @allure.story("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_error(self, order_api, created_user):
        response = order_api.create(
            {"ingredients": []}, token=created_user["token"]
        )

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["message"] == INGREDIENTS_REQUIRED
        assert "order" not in body

    @allure.story("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_error(
        self, order_api, created_user
    ):
        payload = {"ingredients": INVALID_INGREDIENT_HASHES}
        response = order_api.create(payload, token=created_user["token"])

        # Документация не описывает тело ответа — проверяем только код
        assert response.status_code == 500
        