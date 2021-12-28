from unittest.mock import ANY

import pytest
from graphene.relay.node import to_global_id
from graphene.test import Client

from api.graphql import schema
from auth import generate_token
from models import TableBooking, User


@pytest.fixture
def test_client():
    return Client(schema)


def test_resolve_me(test_client, user_factory, db_session, request_factory):
    password = "strongpass!"
    email = "user@test.com"
    user = user_factory(email=email, password=password)
    token = generate_token(user)

    request = request_factory(headers={"Authorization": f"Bearer {token}"})

    query = """
        {
            me {
                email
            }
        }
    """

    response = test_client.execute(
        query, context_value={"session": db_session, "request": request}
    )
    expected = {"me": {"email": user.email}}

    assert response.get("errors") is None
    assert response["data"] == expected


def test_signup_user(test_client, db_session):
    email = "newuser@test.com"
    password = "strongpass!"

    query = """
        mutation m {
             signUp (email: "%s", password: "%s") {
                 user {
                     email
                 }
             }
        }
    """ % (
        email,
        password,
    )
    response = test_client.execute(query, context_value={"session": db_session})
    expected = {"signUp": {"user": {"email": email}}}

    assert response.get("errors") is None
    assert response["data"] == expected
    assert db_session.query(User).filter_by(email=email).first() is not None


def test_signin_user(test_client, db_session, user_factory):
    password = "strongpass!"
    email = "user@test.com"
    _ = user_factory(email=email, password=password)

    query = """
        mutation m {
             signIn (email: "%s", password: "%s") {
                 token
             }
        }
    """ % (
        email,
        password,
    )
    response = test_client.execute(query, context_value={"session": db_session})
    expected = {"signIn": {"token": ANY}}

    assert response.get("errors") is None
    assert response["data"] == expected
    assert db_session.query(User).filter_by(email=email).first() is not None


def test_graphql_up(test_client):
    query = """
        {
            up
        }
    """
    response = test_client.execute(query)
    expected = {"up": True}

    assert response.get("errors") is None
    assert response["data"] == expected


def test_resolve_restaurants(
    test_client, restaurant_factory, db_session, user_factory, request_factory
):
    restaurant = restaurant_factory(name="taverna")
    restaurant_gid = to_global_id("RestaurantNode", restaurant.id)
    user = user_factory(email="test@test.com", password="Test1")
    token = generate_token(user)
    request = request_factory(headers={"Authorization": f"Bearer {token}"})

    query = """
        {
            restaurants {
                edges {
                    node {
                        name
                        id
                    }
                }
            }
        }
    """

    response = test_client.execute(
        query, context_value={"session": db_session, "request": request}
    )
    expected = {
        "restaurants": {
            "edges": [{"node": {"name": restaurant.name, "id": restaurant_gid}}]
        }
    }

    assert response.get("errors") is None
    assert response["data"] == expected


def test_resolve_restaurants_with_paramterized_query(
    test_client, restaurant_factory, db_session, user_factory, request_factory
):
    restaurant = restaurant_factory(name="taverna")
    _ = restaurant_factory(name="americano")
    user = user_factory(email="test@test.com", password="Test1")
    token = generate_token(user)
    request = request_factory(headers={"Authorization": f"Bearer {token}"})
    restaurant_gid = to_global_id("RestaurantNode", restaurant.id)

    query = """
        {
            restaurants (q: "tav", first: 1) {
                edges {
                    node {
                        name
                        id
                    }
                }
            }
        }
    """

    response = test_client.execute(
        query, context_value={"session": db_session, "request": request}
    )
    expected = {
        "restaurants": {
            "edges": [{"node": {"name": restaurant.name, "id": restaurant_gid}}]
        }
    }

    assert response.get("errors") is None
    assert response["data"] == expected


def test_book_table_in_restaurant(
    test_client,
    restaurant_factory,
    table_factory,
    user_factory,
    db_session,
    request_factory,
):
    restaurant = restaurant_factory(name="taverna")
    restaurant_gid = to_global_id("RestaurantNode", restaurant.id)
    _ = table_factory(restaurant=restaurant, max_persons=5, is_open=True)
    user = user_factory(email="tester@example.pl")
    token = generate_token(user)
    request = request_factory(headers={"Authorization": f"Bearer {token}"})
    persons = 3

    query = """
        mutation m {
             bookRestaurantTable (restaurantGid: "%s", persons: %s) {
                 isBooked
             }
        }
    """ % (
        restaurant_gid,
        persons,
    )
    response = test_client.execute(
        query, context_value={"session": db_session, "request": request}
    )
    expected = {"bookRestaurantTable": {"isBooked": True}}

    assert response.get("errors") is None
    assert response["data"] == expected
    assert (
        db_session.query(TableBooking)
        .filter_by(restaurant=restaurant, user=user, persons=persons)
        .first()
        is not None
    )


def test_cancel_table_booking(
    test_client,
    restaurant_factory,
    table_booking_factory,
    user_factory,
    db_session,
    request_factory,
):
    restaurant = restaurant_factory(name="taverna")
    user = user_factory(email="tester@example.pl")
    table_booking = table_booking_factory(restaurant=restaurant, user=user)
    table_booking_gid = to_global_id("TableBookingNode", table_booking.id)
    token = generate_token(user)
    request = request_factory(headers={"Authorization": f"Bearer {token}"})

    query = """
        mutation m {
             cancelTableBooking (tableBookingGid: "%s") {
                 tableBooking {
                     isActive
                     id
                 }
             }
        }
    """ % (
        table_booking_gid
    )
    response = test_client.execute(
        query, context_value={"session": db_session, "request": request}
    )
    expected = {
        "cancelTableBooking": {
            "tableBooking": {"id": table_booking_gid, "isActive": False}
        }
    }

    assert response.get("errors") is None
    assert response["data"] == expected
