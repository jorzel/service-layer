from typing import Optional

from sqlalchemy.orm import Query, Session

from models import Restaurant, TableBooking, User


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
