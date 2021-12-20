import pytest
from graphene.test import Client

from api.graphql import schema


@pytest.fixture
def test_client():
    return Client(schema)


def test_allows_get_with_variable_values(test_client):
    query = """
        {
            up
        }
    """
    response = test_client.execute(query)
    expected = {"up": True}

    assert response.get("errors") is None
    assert response["data"] == expected
