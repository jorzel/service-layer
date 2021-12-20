import pytest


@pytest.fixture
def test_client(app):
    return app.test_client()


def test_up_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json == {"up": True}


def test_get_restaurants(test_client, restaurant_factory, db_session):
    restaurant = restaurant_factory(name="taverna")

    response = test_client.get("/restaurants")
    assert response.status_code == 200
    assert response.json == [{"name": restaurant.name, "id": restaurant.id}]
