#!/usr/bin/python3
"""creates ioute"""
from api.v1.views import app_views
from flask import jsonify
import models
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """return status of json
    A JSON string of status 200 response
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Gets stats for models
    """
    stats_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(stats_dict)
