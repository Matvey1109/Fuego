from pydantic import BaseModel, ValidationError

from fuego.data import FuegoRequest


class RequestSchema(BaseModel):
    """Defines expected request structure."""

    path: str
    method: str


def validate_request(request: FuegoRequest):
    """Validates request data using Pydantic."""
    try:
        RequestSchema(path=request.path, method=request.method)
    except ValidationError as e:
        raise ValueError(f"Invalid request: {e}")
