import json
from typing import Any, Callable, Iterable, Optional


class FuegoRequest:
    """Custom request class for Fuego, compatible with both WSGI and ASGI."""

    def __init__(
        self,
        method: str,
        path: str,
        query_string: str,
        body: bytes,
        scope: Optional[dict] = None,
    ):
        self.method: str = method
        self.path: str = path
        self.query_string: str = query_string
        self.body: str = body.decode("utf-8") if body else ""
        self.scope = scope  # For ASGI requests

    @property
    def json(self) -> dict[str, Any]:
        """Parses and returns JSON data from the request body."""
        try:
            return json.loads(self.body) if self.body else {}
        except ValueError:
            return {}


class FuegoResponse:
    """Custom response class for Fuego, compatible with both WSGI and ASGI."""

    def __init__(self):
        self.status_code: int = 200
        self.headers: dict[str, str] = {"Content-Type": "text/plain"}
        self.body: str = b""

    def set_status(self, status: int):
        """Sets the response status code."""
        self.status_code = status

    def set_header(self, key: str, value: str):
        """Sets a response header."""
        self.headers[key] = value

    def set_body(self, body: str):
        """Sets the response body."""
        self.body = body.encode("utf-8")

    def json(self, data: dict[str, Any], status: int = 200):
        """Sets response to JSON format."""
        self.set_status(status)
        self.set_header("Content-Type", "application/json")
        self.set_body(json.dumps(data))

    def __call__(self, start_response: Callable) -> Iterable[bytes]:
        """WSGI response callable."""
        start_response(f"{self.status_code} OK", list(self.headers.items()))
        return [self.body]
