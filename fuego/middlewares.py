import logging
from datetime import datetime

from fuego import FuegoRequest, FuegoResponse
from fuego.server_type import detect_server_type

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def fuego_logging_middleware(request: FuegoRequest, response: FuegoResponse):
    timestamp = datetime.now().isoformat()

    # Log the request and response status
    server_type: str = detect_server_type(request)
    logger.info(
        f"Fuego Logs 🔥 [{timestamp}] {response.status_code} {request.method} {request.path} (Server: {server_type})"
    )
