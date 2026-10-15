from requests import Response, Session

from data.urls import BASE_URL


class HttpClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self._session = Session()
        self._session.headers.update({"Content-Type": "application/json"})

    def get(self, path: str, headers: dict | None = None) -> Response:
        return self._session.get(
            f"{self.base_url}{path}",
            headers=headers,
        )

    def post(
        self,
        path: str,
        json: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        return self._session.post(
            f"{self.base_url}{path}",
            json=json,
            headers=headers,
        )

    def patch(
        self,
        path: str,
        json: dict | None = None,
        headers: dict | None = None,
    ) -> Response:
        return self._session.patch(
            f"{self.base_url}{path}",
            json=json,
            headers=headers,
        )

    def delete(self, path: str, headers: dict | None = None) -> Response:
        return self._session.delete(
            f"{self.base_url}{path}",
            headers=headers,
        )
    