from typing import Any, Dict

from flask import Blueprint, current_app, jsonify, request

from models import Restaurant
from service import book_restaurant_table

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
    _ = book_restaurant_table(
        session,
        restaurant_id=payload["restaurant_id"],
        user_email=payload["user_email"],
        persons=payload["persons"],
    )
    return jsonify({"isBooked": True}), 201
