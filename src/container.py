from dependency_injector import containers
from dependency_injector import providers
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from typing import Generator

from src.handler.paste.create import CreatePasteRequestHandler
from src.handler.paste.delete import DeletePasteRequestHandler
from src.handler.paste.delete_expired import DeleteExpiredPasteRequestHandler
from src.handler.paste.get import GetPasteRequestHandler
from src.handler.paste.update_view import UpdatePasteViewRequestHandler


def init_session(factory: scoped_session) -> Generator:
    session = factory()

    yield session

    factory.remove()


class HandlersContainer(containers.DeclarativeContainer):
    session = providers.Dependency(instance_of=Session)

    paste_create = providers.Factory(CreatePasteRequestHandler, session=session)
    paste_get = providers.Factory(GetPasteRequestHandler, session=session)
    paste_update_view = providers.Factory(
        UpdatePasteViewRequestHandler, session=session
    )
    paste_delete = providers.Factory(
        DeletePasteRequestHandler, session=session
    )
    paste_delete_expired = providers.Factory(
        DeleteExpiredPasteRequestHandler, session=session
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_engine = providers.Singleton(create_engine, config.db_connection)
    session_factory = providers.Factory(
        sessionmaker, bind=db_engine, expire_on_commit=False, autoflush=False
    )
    scoped_session = providers.Factory(scoped_session, session_factory)
    session = providers.Resource(init_session, factory=scoped_session)

    handlers = providers.Container(HandlersContainer, session=session)
