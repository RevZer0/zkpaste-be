import pytest
from datetime import datetime
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Callable
from typing import Generator

from src.domain.paste import Paste


@pytest.fixture
def api_client() -> TestClient:
    from src.application import application

    return TestClient(application)


@pytest.fixture
def session_factory() -> Callable[..., Session]:
    from src.application import container

    return container.session_factory.provided()


@pytest.fixture
def persisted_paste_factory(
    session_factory: Callable[..., Session], faker: Faker
) -> Generator:
    created_instances = []

    def maker(
        ttl: int = 60,
        date_created: datetime | None = None,
        opens_limit: int | None = None,
        current_opens: int = 0,
    ) -> Paste:
        with session_factory() as s:
            paste = Paste.init(
                faker.binary(length=128),
                faker.binary(length=12),
                faker.binary(length=32),
                False,
                ttl,
                opens_limit,
            )
            if date_created:
                paste.date_created = date_created

            if current_opens:
                paste.current_opens = current_opens

            s.add(paste)
            s.commit()
            created_instances.append(paste)
        return paste

    yield maker

    with session_factory() as s:
        s.add_all(created_instances)
        [s.delete(i) for i in created_instances]
        s.commit()
