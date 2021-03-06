#!/usr/bin/python3
"""API routes"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def show_cities_by_state(state_id):
    """Returns a list of all City objects by State
    """
    city_array = []
    state = storage.get(State, state_id)
    if state is not None:
        for city in state.cities:
            city_array.append(city.to_dict())
        return jsonify(city_array)

    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def show_one_city(city_id):
    """Shows a specific state based on id
    """
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a state based on storage id
    """
    city_to_delete = storage.get(City, city_id)
    if city_to_delete is None:
        abort(404)
    # city_to_delete.delete()
    storage.delete(city_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create state object
    """
    if storage.get(State, state_id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    json_request = request.get_json()
    if "name" not in json_request:
        return jsonify({"error": "Missing name"}), 400
    else:
        # city_name = city_dict["name"]
        # city = City(name=city_name, state_id=state_id)
        city = City(**json_request)
        for key, value in json_request.items():
            setattr(city, key, value)
        setattr(city, "state_id", state_id)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates an existing city object based on the id
           Returns:
               A JSON dictionary of the udpated state in a 200 response
               400 response if not dict)
               404 response if the id does not match a storage id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    req.pop("id", None)
    req.pop("state_id", None)
    req.pop("created_at", None)
    req.pop("updated_at", None)
    for key, val in req.items():
        setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
