import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Callable


@pytest.fixture
def api_client() -> TestClient:
    from src.application import application

    return TestClient(application)

@pytest.fixture
def session_factory() -> Callable[..., Session]:
    from src.application import container

    return container.session_factory.provided()
