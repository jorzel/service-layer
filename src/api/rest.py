from typing import Any, Dict

from flask import Blueprint, current_app, jsonify

from models import Restaurant

main = Blueprint("main", __name__)


def restaurant_serializer(restaurant: Restaurant) -> Dict[str, Any]:
    return {"id": restaurant.id, "name": restaurant.name}


@main.route("/")
def up():
    return jsonify({"up": True})


@main.route("/restaurants", methods=["GET"])
def restaurants():
    session = current_app.session
    restaurants = [restaurant_serializer(r) for r in session.query(Restaurant)]
    return jsonify(restaurants)
