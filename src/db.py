from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import configure_mappers, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///dev.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


from models import *  # noqa

configure_mappers()

# should be called once or moved to separated script in order to create db tables
# Base.metadata.create_all(engine)
