import base64
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Callable

from src.domain.paste import Paste


def test_delete_paste(
        api_client: TestClient, 
        persisted_paste_factory: Callable[..., Paste], 
        session_factory: Callable[..., Session]
) -> None:
    paste = persisted_paste_factory()
    response = api_client.post(
        '/paste/{}/delete'.format(paste.id), 
        headers={'Content-type': 'application/json'}, 
        json={'signature': base64.b64encode(paste.signature).decode()}
    )
    assert response.status_code == 200
    with session_factory() as s:
        check = s.get(Paste, paste.id)
        assert check is None

def test_delete_paste_with_invalid_signature(
        api_client: TestClient, 
        persisted_paste_factory: Callable[..., Paste], 
        session_factory: Callable[..., Session],
        faker: Faker
) -> None:
    paste = persisted_paste_factory()
    response = api_client.post(
        '/paste/{}/delete'.format(paste.id), 
        headers={'Content-type': 'application/json'}, 
        json={'signature': base64.b64encode(faker.sentence().encode()).decode()}
    )
    assert response.status_code == 200
    with session_factory() as s:
        check = s.get(Paste, paste.id)
        assert check is not None
