import pytest
from graphene.test import Client

from api.graphql import schema


@pytest.fixture
def test_client():
    return Client(schema)


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

    query = """
        {
            restaurants {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """

    response = test_client.execute(query, context_value={"session": db_session})
    expected = {"restaurants": {"edges": [{"node": {"name": restaurant.name}}]}}

    assert response.get("errors") is None
    assert response["data"] == expected
