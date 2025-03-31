from typing import Callable, Iterable, Optional

from parse import parse

from fuego.data import FuegoRequest, FuegoResponse
from fuego.validation import validate_request


class Fuego:
    """Minimal web framework."""

    def __init__(self):
        self.routes: dict[str, dict[str, Callable]] = {}
        self.middlewares: list[Callable] = []

    def route(self, path: str, method: str):
        """Registers a route with a handler."""

        def wrapper(handler: Callable):
            self.routes.setdefault(path, {})[method] = handler
            return handler

        return wrapper

    def register_middleware(self, middleware: Callable):
        """Registers a middleware function."""
        self.middlewares.append(middleware)

    def handle_request(self, request: FuegoRequest) -> FuegoResponse:
        """Processes the HTTP request and returns a response."""
        response = FuegoResponse()
        handler, kwargs = self.find_handler(request.path, request.method)

        if handler:
            validate_request(request)  # Validate request data
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        for middleware in self.middlewares:
            middleware(request, response)

        return response

    def find_handler(
        self, path: str, method: str
    ) -> tuple[Optional[Callable], Optional[dict]]:
        """Finds the correct route handler for a request."""
        for route, methods in self.routes.items():
            parsed_result = parse(route, path)
            if parsed_result and method in methods:
                return methods[method], parsed_result.named

        return None, None

    def default_response(self, response: FuegoResponse):
        """Returns a 404 response for unknown routes."""
        response.json(
            data={"message": "Not Found"},
            status=404,
        )

    def get_wsgi_app(self) -> Callable:
        """Returns a WSGI callable bound to this instance."""

        def wsgi_app(environ: dict, start_response: Callable) -> Iterable[bytes]:
            """
            WSGI application entry.

            Args:
                environ (dict): Dictionary containing WSGI environment variables
                start_response (Callable): Function that starts the WSGI response

            Returns:
                Iterable[bytes]: Response body as an iterable object of bytes
            """
            request = FuegoRequest(
                method=environ["REQUEST_METHOD"],
                path=environ["PATH_INFO"],
                query_string=environ.get("QUERY_STRING", ""),
                body=environ.get("wsgi.input", b"").read(),
            )
            response = self.handle_request(request)
            return response(start_response)

        return wsgi_app

    def get_asgi_app(self) -> Callable:
        """Returns an ASGI callable bound to this instance."""

        async def asgi_app(scope: dict, receive: Callable, send: Callable) -> None:
            """
            ASGI application entry point.

            Args:
                scope (dict): ASGI scope containing request information
                receive (Callable): Async function to receive incoming events
                send (Callable): Async function to send response events
            """
            if scope["type"] != "http":
                return

            body = b""
            while True:
                message = await receive()
                if message["type"] == "http.request":
                    body += message.get("body", b"")
                    if not message.get("more_body", False):
                        break

            request = FuegoRequest(
                method=scope["method"],
                path=scope["path"],
                query_string=scope.get("query_string", b"").decode("utf-8"),
                body=body,
                scope=scope,
            )
            response = self.handle_request(request)

            await send(
                {
                    "type": "http.response.start",
                    "status": response.status_code,
                    "headers": [
                        (key.encode("utf-8"), value.encode("utf-8"))
                        for key, value in response.headers.items()
                    ],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": response.body,
                }
            )

        return asgi_app
