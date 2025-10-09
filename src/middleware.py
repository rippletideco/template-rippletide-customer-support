import logging
from time import time

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def init_middleware(app: FastAPI):
    app.add_middleware(CorrelationIdMiddleware)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time()

        response: Response = await call_next(request)

        process_time = (time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        rid_header = response.headers.get("X-Request-Id")
        request_id = rid_header or response.headers.get("X-Blaxel-Request-Id")
        if response.status_code >= 400:
            logger.error(
                f"{request.method} {request.url.path} {response.status_code} {formatted_process_time}ms rid={request_id}"
            )
        else:
            logger.info(
                f"{request.method} {request.url.path} {response.status_code} {formatted_process_time}ms rid={request_id}"
            )

        return response

def init_error_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, e: Exception):
        logger.error(f"Error during request: {e}", exc_info=e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"error": str(e)}),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, e: HTTPException):
        logger.error(f"Error during request: {e}", exc_info=e)
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder({"error": str(e)}),
        )

