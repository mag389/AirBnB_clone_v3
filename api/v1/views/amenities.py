#!/usr/bin/python3
""" amenity view file """
from api.v1.views import app_views
from flask import jsonify, request, abort
import models
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def get_amenity():
    """ routing for retrieving all amenities """
    amens = storage.all(Amenity).values()
    retval = []
    for obj in amens:
        retval.append(obj.to_dict())
    return jsonify(retval)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def get_from_id(amenity_id):
    """ gets an amenity from an amenity id """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ deletes an amenity form id """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    storage.delete(amen)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def amenity_post():
    """ creates new amenity object """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    new_am = models.amenity.Amenity(**req)
    new_am.save()
    return jsonify(new_am.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def amenity_update(amenity_id):
    """ updates the amenity """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    req.pop("id", None)
    req.pop("created_at", None)
    req.pop("updated_at", None)
    for key, val in req.items():
        setattr(amen, key, val)
    amen.save()
    return jsonify(amen.to_dict()), 200
