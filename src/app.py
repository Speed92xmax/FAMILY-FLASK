"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member(
    {
        "id": jackson_family._generateId(),
        "first_name": "John",
        "last_name": jackson_family.last_name,
        "age": 33,
        "lucky_numbers": [7, 13, 22],
    },
)

jackson_family.add_member(
    {
        "id": jackson_family._generateId(),
        "first_name": "Jane",
        "last_name": jackson_family.last_name,
        "age": 35,
        "lucky_numbers": [10, 14, 3],
    }
)

jackson_family.add_member(
    {
        "id": jackson_family._generateId(),
        "first_name": "Jimmy",
        "last_name": jackson_family.last_name,
        "age": 5,
        "lucky_numbers": [1],
    }
)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/members", methods=["GET"])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route("/member", methods=["POST"])
def create_member():
    body = request.json
    first_name = body.get("first_name", None)
    age = body.get("age", None)
    lucky_numbers = body.get("lucky_numbers", None)

    if first_name is None or age is None or lucky_numbers is None:
        return jsonify({"error": "Inputs can't be empty"}), 400

    jackson_family.add_member(body)

    return jsonify({"msg": "Family member created"}), 200


@app.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):

    member = jackson_family.get_member(member_id)
    print(member)
    if member is None:
        return jsonify({"error": "user not found"}), 400

    return jsonify(member), 200


@app.route("/member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):

    if jackson_family.delete_member(member_id) is None:
        return jsonify({"error": "user not found for delete"}), 400

    return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
