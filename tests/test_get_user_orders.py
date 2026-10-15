import allure

from data.errors import AUTH_REQUIRED
from data.order_data import DEFAULT_INGREDIENTS_COUNT


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.story("Получение заказов авторизованным пользователем")
    def test_get_orders_with_auth_success(
        self, order_api, created_user, available_ingredient_ids
    ):
        order_api.create(
            {"ingredients": available_ingredient_ids[:DEFAULT_INGREDIENTS_COUNT]},
            token=created_user["token"],
        )

        response = order_api.get_user_orders(token=created_user["token"])

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "orders" in body
        assert isinstance(body["orders"], list)
        assert len(body["orders"]) >= 1
        assert body["total"] >= 1
        assert "totalToday" in body

    @allure.story("Получение заказов неавторизованным пользователем")
    def test_get_orders_without_auth_error(self, order_api):
        response = order_api.get_user_orders_without_token()

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == AUTH_REQUIRED
        assert "orders" not in body

        