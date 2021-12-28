from typing import Any, Dict

from flask import Blueprint, current_app, jsonify, request

from models import Restaurant, Table
from service import book_restaurant_table, get_restaurants

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
    query = get_restaurants(
        session, search=request.args.get("q"), limit=request.args.get("limit")
    )
    restaurants = [restaurant_serializer(r) for r in query]
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


@main.route("/add", methods=["GET"])
def add():
    session = current_app.session
    restaurant = Restaurant(name="taverna")
    session.add(restaurant)
    session.flush()
    table = Table(max_persons=10, restaurant=restaurant)
    session.add(table)
    session.commit()

    return "success"
