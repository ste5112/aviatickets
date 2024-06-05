from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton

from database import SessionLocal
from tickets.repos.tickets_repo import TicketsRepo
from tickets.service.tickets_service import TicketsService


class AppContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["tickets"])

    _session_factory: Singleton = Singleton(SessionLocal)

    tickets_repo: Singleton = Singleton(TicketsRepo, session_factory=_session_factory)
    tickets_service: Singleton = Singleton(
        TicketsService,
        repo=tickets_repo,
    )
