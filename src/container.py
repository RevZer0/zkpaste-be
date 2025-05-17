from dependency_injector import containers
from dependency_injector import providers
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from typing import Generator

from src.handler.paste.get import GetPasteRequestHandler

from .handler.paste.create import CreatePasteRequestHandler


def init_session(factory: scoped_session) -> Generator:
    session = factory()

    yield session

    factory.remove()


class HandlersContainer(containers.DeclarativeContainer):
    session = providers.Dependency(instance_of=Session)

    paste_create = providers.Factory(CreatePasteRequestHandler, session=session)
    paste_get = providers.Factory(GetPasteRequestHandler, session=session)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_engine = providers.Singleton(create_engine, config.db_connection)
    session_factory = providers.Factory(
        sessionmaker, bind=db_engine, expire_on_commit=False, autoflush=False
    )
    scoped_session = providers.Factory(scoped_session, session_factory)
    session = providers.Resource(init_session, factory=scoped_session)

    handlers = providers.Container(HandlersContainer, session=session)
