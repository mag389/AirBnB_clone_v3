#!/usr/bin/python3
""" amenity view file """
from api.v1.views import app_views
from flask import jsonify, request, abort
import models
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=['GET'])
def get_all_users():
    """ routing for retrieving all users """
    users = storage.all(User).values()
    retval = []
    for obj in users:
        retval.append(obj.to_dict())
    return jsonify(retval)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['GET'])
def get_one_user(user_id):
    """ gets an amenity from an amenity id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """ deletes a user from id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def postcreate_user():
    """ creates new amenity object """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "email" not in req:
        abort(400, "Missing email")
    if "password" not in req:
        abort(400, "Missing password")
    new_user = models.user.User(**req)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['PUT'])
def user_update(user_id):
    """ updates the user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    req.pop("id", None)
    req.pop("email", None)
    req.pop("created_at", None)
    req.pop("updated_at", None)
    for key, val in req.items():
        setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
