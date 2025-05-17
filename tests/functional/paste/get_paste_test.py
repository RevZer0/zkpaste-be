import base64
from collections.abc import Callable
from datetime import datetime
from datetime import timedelta
from fastapi.testclient import TestClient

from src.domain.paste import Paste


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
    api_client: TestClient, persisted_paste_factory: Callable[..., Paste]
) -> None:
    paste = persisted_paste_factory(
        ttl=10, date_created=datetime.now() - timedelta(minutes=1)
    )
    response = api_client.get(
        "/paste/{}".format(paste.id), headers={"Content-type": "application/json"}
    )
    assert response.status_code == 404


def test_open_counts_exceeded(
    api_client: TestClient, persisted_paste_factory: Callable[..., Paste]
) -> None:
    paste = persisted_paste_factory(opens_limit=10, current_opens=10)
    response = api_client.get(
        "/paste/{}".format(paste.id), headers={"Content-type": "application/json"}
    )
    assert response.status_code == 404
