from requests import Response

from api.http_client import HttpClient
from data.urls import OrderEndpoints


class OrderApi:
    def __init__(self, client: HttpClient):
        self.client = client

    def get_ingredients(self) -> Response:
        return self.client.get(OrderEndpoints.INGREDIENTS)

    def create(self, payload: dict, token: str) -> Response:
        return self.client.post(
            OrderEndpoints.ORDERS,
            json=payload,
            headers={"Authorization": token},
        )

    def create_without_token(self, payload: dict) -> Response:
        return self.client.post(OrderEndpoints.ORDERS, json=payload)

    def get_user_orders(self, token: str) -> Response:
        return self.client.get(
            OrderEndpoints.ORDERS,
            headers={"Authorization": token},
        )

    def get_user_orders_without_token(self) -> Response:
        return self.client.get(OrderEndpoints.ORDERS)
    