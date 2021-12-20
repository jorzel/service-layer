import pytest


@pytest.fixture
def test_client(app):
    return app.test_client()


def test_up_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json == {"up": True}
