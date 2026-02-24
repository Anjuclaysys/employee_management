import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.

    Logs:
    - HTTP method
    - Request path
    - Response status code
    - Processing time
    - Unhandled exceptions (with traceback)

    This middleware wraps every incoming HTTP request.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process incoming request and log execution details.

        :param request: Incoming HTTP request.
        :type request: Request
        :param call_next: Next middleware or route handler.
        """
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(
                f"unhandled exception  {str(e)}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                },
            )
            raise
        process_time = time.perf_counter() - start_time
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": round(process_time, 4),
            },
        )
        return response
