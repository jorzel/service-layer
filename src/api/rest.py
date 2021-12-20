from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/")
def up():
    return jsonify({"up": True})
