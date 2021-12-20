import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import SQLALCHEMY_DATABASE_URL, Base
from models import Restaurant
from setup import create_app


@pytest.fixture(scope="session")
def db_connection():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    connection = engine.connect()

    yield connection

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(db_connection):
    transaction = db_connection.begin()
    session = sessionmaker(bind=db_connection)
    db_session = session()

    yield db_session

    transaction.rollback()
    db_session.close()


@pytest.fixture
def app(db_session):
    app = create_app()
    app.session = db_session
    return app


@pytest.fixture
def restaurant_factory(db_session):
    def _restaurant_factory(**kwargs):
        restaurant = Restaurant(**kwargs)
        db_session.add(restaurant)
        db_session.flush()
        return restaurant

    yield _restaurant_factory
