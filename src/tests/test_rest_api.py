import pytest

from models import TableBooking


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


def test_post_bookings(
    test_client, restaurant_factory, table_factory, user_factory, db_session
):
    restaurant = restaurant_factory(name="taverna")
    _ = table_factory(restaurant=restaurant, max_persons=5, is_open=True)
    user = user_factory(email="tester@example.pl")
    persons = 3
    payload = {
        "restaurant_id": restaurant.id,
        "persons": persons,
        "user_email": user.email,
    }

    response = test_client.post("/bookings", json=payload)

    assert response.status_code == 201
    assert response.json == {"isBooked": True}
    assert (
        db_session.query(TableBooking)
        .filter_by(user=user, restaurant=restaurant, persons=persons)
        .first()
    )
