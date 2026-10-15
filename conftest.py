import pytest

from api.http_client import HttpClient
from api.order_api import OrderApi
from api.user_api import UserApi
from data.user_data import generate_unique_user


@pytest.fixture(scope="session")
def http_client():
    return HttpClient()


@pytest.fixture(scope="session")
def user_api(http_client):
    return UserApi(http_client)


@pytest.fixture(scope="session")
def order_api(http_client):
    return OrderApi(http_client)


@pytest.fixture
def created_user(user_api):
    user_data = generate_unique_user()
    response = user_api.register(user_data)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    token = response.json()["accessToken"]

    user = {**user_data, "token": token}
    yield user

    user_api.delete(token=token)


@pytest.fixture
def second_user(user_api):
    user_data = generate_unique_user()
    response = user_api.register(user_data)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    token = response.json()["accessToken"]

    user = {**user_data, "token": token}
    yield user

    user_api.delete(token=token)


@pytest.fixture
def cleanup_user(user_api):
    tokens: list[str] = []

    def register_token(token: str) -> None:
        tokens.append(token)

    yield register_token

    for token in tokens:
        user_api.delete(token=token)


@pytest.fixture(scope="session")
def available_ingredient_ids(order_api):
    response = order_api.get_ingredients()
    assert response.status_code == 200
    return [item["_id"] for item in response.json()["data"]]