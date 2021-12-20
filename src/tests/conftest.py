import pytest

from setup import create_app


@pytest.fixture
def app():
    return create_app()
