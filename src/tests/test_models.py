from models import Restaurant


def test_add_restuarant_instance(restaurant_factory, db_session):
    restaurant = restaurant_factory(name="test")

    assert (
        db_session.query(Restaurant).filter_by(name=restaurant.name).first() is not None
    )
