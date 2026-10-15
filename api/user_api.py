from requests import Response

from api.http_client import HttpClient
from data.urls import UserEndpoints


class UserApi:
    def __init__(self, client: HttpClient):
        self.client = client

    def register(self, payload: dict) -> Response:
        return self.client.post(UserEndpoints.REGISTER, json=payload)

    def login(self, payload: dict) -> Response:
        return self.client.post(UserEndpoints.LOGIN, json=payload)

    def update(self, payload: dict, token: str) -> Response:
        return self.client.patch(
            UserEndpoints.USER,
            json=payload,
            headers={"Authorization": token},
        )

    def update_without_token(self, payload: dict) -> Response:
        return self.client.patch(UserEndpoints.USER, json=payload)

    def delete(self, token: str) -> Response:
        return self.client.delete(
            UserEndpoints.USER,
            headers={"Authorization": token},
        )
    