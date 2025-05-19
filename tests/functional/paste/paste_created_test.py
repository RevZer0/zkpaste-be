import base64
import random
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Callable

from src.domain.paste import Paste


def test_create_paste(
    api_client: TestClient, faker: Faker, session_factory: Callable[..., Session]
) -> None:
    payload = {
        "ciphertext": base64.b64encode(faker.paragraph().encode()).decode(),
        "iv": base64.b64encode(random.randbytes(12)).decode(),
        "signature": base64.b64encode(random.randbytes(32)).decode(),
        "metadata": {},
    }

    response = api_client.post(
        "/paste", json=payload, headers={"Content-type": "application/json"}
    )
    assert response.status_code == 200
    assert "paste_id" in response.json()

    with session_factory() as s:
        paste = s.get(Paste, response.json()["paste_id"])
        assert paste is not None

        assert len(paste.paste) > 0
        assert len(paste.iv) == 12
        assert len(paste.signature) == 32
        assert paste.password_protected is False
        assert paste.ttl == 86400
        assert paste.opens_limit is None
        assert paste.current_opens == 0
        assert paste.date_created is not None

        s.delete(paste)
        s.commit()


def test_invalid_base64_data(api_client: TestClient, faker: Faker) -> None:
    payload = {
        "ciphertext": faker.paragraph(),
        "iv": base64.b64encode(random.randbytes(12)).decode(),
        "signature": base64.b64encode(random.randbytes(32)).decode(),
        "metadata": {},
    }

    response = api_client.post(
        "/paste", json=payload, headers={"Content-type": "application/json"}
    )
    assert response.status_code == 409


def test_invalid_iv_len(api_client: TestClient, faker: Faker) -> None:
    payload = {
        "ciphertext": base64.b64encode(faker.paragraph().encode()).decode(),
        "iv": base64.b64encode(random.randbytes(5)).decode(),
        "signature": base64.b64encode(random.randbytes(32)).decode(),
        "metadata": {},
    }

    response = api_client.post(
        "/paste", json=payload, headers={"Content-type": "application/json"}
    )
    assert response.status_code == 409


def test_invalid_signature_len(api_client: TestClient, faker: Faker) -> None:
    payload = {
        "ciphertext": base64.b64encode(faker.paragraph().encode()).decode(),
        "iv": base64.b64encode(random.randbytes(12)).decode(),
        "signature": base64.b64encode(random.randbytes(16)).decode(),
        "metadata": {},
    }

    response = api_client.post(
        "/paste", json=payload, headers={"Content-type": "application/json"}
    )
    assert response.status_code == 409
