#!/usr/bin/python3
""" places reviews routing file """
from api.v1.views import app_views
from flask import jsonify, request, abort
import models
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def get_all_reviews():
    """ routing for retrieving reviews by palce """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review).values()
    retval = []
    for obj in reviews:
        if obj.place_id == place.id:
            retval.append(obj.to_dict())
    return jsonify(retval)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET'])
def get_one_review(review_id):
    """ gets an review from an review id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_review(user_id):
    """ deletes a review from id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=['POST'])
def postcreate_review(place_id):
    """ creates new review object """
    req = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if req is None:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req["user_id"])
    if user is None:
        abort(404)
    if "text" not in req.keys():
        abort(400, "Missing text")
    new_review = models.review.Review(**req)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['PUT'])
def review_update(review_id):
    """ updates the review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    req.pop("id", None)
    req.pop("user_id", None)
    req.pop("place_id", None)
    req.pop("created_at", None)
    req.pop("updated_at", None)
    for key, val in req.items():
        setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
