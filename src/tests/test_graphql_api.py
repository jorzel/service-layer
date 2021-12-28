import pytest
from graphene.relay.node import to_global_id
from graphene.test import Client

from api.graphql import schema
from models import TableBooking, User


@pytest.fixture
def test_client():
    return Client(schema)


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


def test_resolve_restaurants(test_client, restaurant_factory, db_session):
    restaurant = restaurant_factory(name="taverna")
    restaurant_gid = to_global_id("RestaurantNode", restaurant.id)

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

    response = test_client.execute(query, context_value={"session": db_session})
    expected = {
        "restaurants": {
            "edges": [{"node": {"name": restaurant.name, "id": restaurant_gid}}]
        }
    }

    assert response.get("errors") is None
    assert response["data"] == expected


def test_resolve_restaurants_with_paramterized_query(
    test_client, restaurant_factory, db_session
):
    restaurant = restaurant_factory(name="taverna")
    _ = restaurant_factory(name="americano")

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

    response = test_client.execute(query, context_value={"session": db_session})
    expected = {
        "restaurants": {
            "edges": [{"node": {"name": restaurant.name, "id": restaurant_gid}}]
        }
    }

    assert response.get("errors") is None
    assert response["data"] == expected


def test_book_table_in_restaurant(
    test_client, restaurant_factory, table_factory, user_factory, db_session
):
    restaurant = restaurant_factory(name="taverna")
    restaurant_gid = to_global_id("RestaurantNode", restaurant.id)
    _ = table_factory(restaurant=restaurant, max_persons=5, is_open=True)
    user = user_factory(email="tester@example.pl")
    persons = 3

    query = """
        mutation m {
             bookRestaurantTable (restaurantGid: "%s", persons: %s, userEmail: "%s") {
                 isBooked
             }
        }
    """ % (
        restaurant_gid,
        persons,
        user.email,
    )
    response = test_client.execute(query, context_value={"session": db_session})
    expected = {"bookRestaurantTable": {"isBooked": True}}

    assert response.get("errors") is None
    assert response["data"] == expected
    assert (
        db_session.query(TableBooking)
        .filter_by(restaurant=restaurant, user=user, persons=persons)
        .first()
        is not None
    )
