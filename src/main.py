import os
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .middleware import init_middleware, init_error_handlers
from .agent import router


logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Server running on port {os.getenv('PORT', 80)}")
    yield
    logger.info("Server shutting down")


app = FastAPI(lifespan=lifespan)
init_error_handlers(app)
init_middleware(app)

app.include_router(router)


FastAPIInstrumentor.instrument_app(app, exclude_spans=["receive", "send"])
