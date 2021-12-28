from typing import Optional

from sqlalchemy.orm import Query, Session

from auth import generate_password_hash
from models import Restaurant, TableBooking, User


class UserAlreadyExist(Exception):
    pass


def book_restaurant_table(
    session: Session, restaurant_id: int, user_email: str, persons: int
) -> TableBooking:
    user = session.query(User).filter_by(email=user_email).first()
    restaurant = session.query(Restaurant).get(restaurant_id)
    table_booking = restaurant.book_table(persons, user)
    session.add(table_booking)
    session.commit()
    return table_booking


def get_restaurants(
    session: Session, search: Optional[str] = None, limit: Optional[int] = None
) -> Query:
    filter_args = []
    if search:
        filter_args.append(Restaurant.name.ilike(f"%{search}%"))
    query = session.query(Restaurant).filter(*filter_args)
    if limit:
        query = query.limit(limit)
    return query


def sign_up(session: Session, email: str, password) -> User:
    if session.query(User).filter_by(email=email).first():
        raise UserAlreadyExist()
    user = User(email=email, password=generate_password_hash(password))
    session.add(user)
    session.commit()
    return user
