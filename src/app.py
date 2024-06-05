import sys
from contextlib import asynccontextmanager

from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI
from structlog import getLogger

from container import AppContainer
from log import setup_logging
from tickets.routes.router import api_router as tickets_router

setup_logging()
logger = getLogger(__name__)


class App(FastAPI):
    container: DeclarativeContainer


@asynccontextmanager
async def lifespan(app: App):
    logger.info("app startup")
    app.include_router(tickets_router)
    yield
    logger.info("app shutdown")


app = App(
    title="Tickets API",
    lifespan=lifespan,
)
app.container = AppContainer()

logger.info("app created")
