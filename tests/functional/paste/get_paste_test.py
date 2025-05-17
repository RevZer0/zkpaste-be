import base64
import pytest
from collections.abc import Callable
from datetime import datetime
from datetime import timedelta
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Generator

from src.domain.paste import Paste


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


def test_get_paste(
    api_client: TestClient, persisted_paste_factory: Callable[..., Paste]
) -> None:
    paste = persisted_paste_factory()
    response = api_client.get(
        "/paste/{}".format(paste.id), headers={"Content-type": "application/json"}
    )
    assert response.status_code == 200
    json = response.json()

    assert json['paste_id'] == str(paste.id)
    assert json['paste'] == base64.b64encode(paste.paste).decode()
    assert json['iv'] == base64.b64encode(paste.iv).decode()


def test_expired_paste(
    api_client: TestClient, persisted_paste_factory: Callable[..., Session]
) -> None:
    paste = persisted_paste_factory(
        ttl=10, date_created=datetime.now() - timedelta(minutes=1)
    )
    response = api_client.get(
        "/paste/{}".format(paste.id), headers={"Content-type": "application/json"}
    )
    assert response.status_code == 404


def test_open_counts_exceeded(
    api_client: TestClient, persisted_paste_factory: Callable[..., Session]
) -> None:
    paste = persisted_paste_factory(opens_limit=10, current_opens=10)
    response = api_client.get(
        "/paste/{}".format(paste.id), headers={"Content-type": "application/json"}
    )
    assert response.status_code == 404
