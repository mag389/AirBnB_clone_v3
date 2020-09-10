#!/usr/bin/python3
""" amenity view file """
from api.v1.views import app_views
from flask import jsonify, request, abort
import models
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=['GET'])
def get_places(city_id):
    """ routing for retrieving all places """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place).values()
    retval = []
    for obj in places:
        if obj.id == city.id:
            retval.append(obj.to_dict())
    return jsonify(retval)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def get_place_from_id(place_id):
    """ gets an place from a place id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """ deletes a place from id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=['POST'])
def place_post(city_id):
    """ creates new place object """
    req = request.get_json()
    if storage.get(City, city_id) is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    if storage.get(User, req["user_id"]) is None:
        abort(404)
    if "name" not in req:
        abort(400, "Missing name")
    req["city_id"] = city_id
    new_place = models.place.Place(**req)
    # setattr(new_place, "city_id", city_id)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['PUT'])
def place_update(place_id):
    """ updates the place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    req.pop("id", None)
    req.pop("created_at", None)
    req.pop("updated_at", None)
    req.pop("user_id", None)
    req.pop("city_id", None)
    for key, val in req.items():
        setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200
