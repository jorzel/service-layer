from typing import Any, Dict

from flask import Blueprint, current_app, jsonify, request

from models import Restaurant, User

main = Blueprint("main", __name__)


def restaurant_serializer(restaurant: Restaurant) -> Dict[str, Any]:
    return {"id": restaurant.id, "name": restaurant.name}


@main.route("/")
@main.route("/up")
def up():
    return jsonify({"up": True})


@main.route("/restaurants", methods=["GET"])
def restaurants():
    session = current_app.session
    restaurants = [restaurant_serializer(r) for r in session.query(Restaurant)]
    return jsonify(restaurants)


@main.route("/bookings", methods=["POST"])
def bookings():
    session = current_app.session
    payload = request.get_json()
    user_email = payload["user_email"]  # it should be done by token of course
    restaurant_id = request.json["restaurant_id"]
    persons = request.json["persons"]
    user = session.query(User).filter_by(email=user_email).first()
    restaurant = session.query(Restaurant).get(restaurant_id)
    table_booking = restaurant.book_table(persons, user)
    session.add(table_booking)
    session.commit()
    return jsonify({"isBooked": True}), 201
