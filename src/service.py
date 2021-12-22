from sqlalchemy.orm import Session

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
