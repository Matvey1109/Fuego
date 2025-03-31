from typing import Union

from fuego.data import FuegoRequest


def detect_server_type(request: Union[FuegoRequest, object]) -> str:
    """Get server type (ASGI or WSGI)."""
    return "ASGI" if request.scope else "WSGI"
