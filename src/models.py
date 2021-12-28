from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class NoOpenTable(Exception):
    pass


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
    table_bookings = relationship("TableBooking")


class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    max_persons = Column(Integer, nullable=False, default=2)
    is_open = Column(Boolean, default=True, nullable=False)
    restaurant_id = Column(ForeignKey("restaurant.id"))
    restaurant = relationship("Restaurant")

    def book(self):
        self.is_open = False


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    tables = relationship("Table", lazy="dynamic")

    def book_table(self, persons: int, user: User):
        table = self._get_open_table(persons)
        if not table:
            raise NoOpenTable()
        table.book()
        return TableBooking(user=user, restaurant=self, persons=persons)

    def _get_open_table(self, persons) -> Optional[Table]:
        return self.tables.filter(
            Table.is_open.is_(True), Table.max_persons >= persons
        ).first()


class TableBooking(Base):
    __tablename__ = "table_booking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booked_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User")
    restaurant_id = Column(ForeignKey("restaurant.id"), nullable=False)
    restaurant = relationship("Restaurant")
    persons = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)

    def cancel(self) -> None:
        self.is_active = False
