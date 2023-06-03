from contextlib import asynccontextmanager

from fastapi import FastAPI
from structlog import getLogger

from container import AppContainer
from log import setup_logging
from tickets.routes.router import api_router as tickets_router

setup_logging()
logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app startup")
    app.container = AppContainer()
    app.include_router(tickets_router)

    yield
    logger.info("app shutdown")


app = FastAPI(
    title="Tickets API",
    lifespan=lifespan,
)

logger.info("app created")
