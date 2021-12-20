from models import Restaurant


def test_add_restuarant_instance(db_session):
    restaurant = Restaurant(name="test")
    db_session.add(restaurant)
    db_session.flush()

    assert db_session.query(Restaurant).filter_by(name="test").first() is not None
