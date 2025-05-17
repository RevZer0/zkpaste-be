import base64
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Callable

from src.domain.paste import Paste


def test_update_paste_view(
    api_client: TestClient,
    persisted_paste_factory: Callable[..., Paste],
    session_factory: Callable[..., Session],
) -> None:
    paste = persisted_paste_factory()

    response = api_client.put(
        '/paste/{}/view'.format(paste.id),
        headers={'Content-type': 'application/json'},
        json={'signature': base64.b64encode(paste.signature).decode()},
    )
    assert response.status_code == 200
    with session_factory() as s:
        s.add(paste)
        s.refresh(paste)

        assert paste.current_opens == 1


def test_update_paste_view_fails_with_wrong_signature(
    api_client: TestClient,
    persisted_paste_factory: Callable[..., Paste],
    session_factory: Callable[..., Session],
    faker: Faker,
) -> None:
    paste = persisted_paste_factory()

    response = api_client.put(
        '/paste/{}/view'.format(paste.id),
        headers={'Content-type': 'application/json'},
        json={'signature': base64.b64encode(faker.sentence().encode()).decode()},
    )
    assert response.status_code == 200
    with session_factory() as s:
        s.add(paste)
        s.refresh(paste)

        assert paste.current_opens == 0
