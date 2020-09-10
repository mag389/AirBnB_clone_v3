#!/usr/bin/python3
"""API routes"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def show_states():
    """Shows all states in storage
    """
    states = list(storage.all('State').values())
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def show_state(state_id):
    """Shows a specific state based on id
    """
    states_list = storage.all("State")
    full_id = "State." + state_id
    try:
        state_object = states_list.get(full_id).to_dict()
        return jsonify(state_object)
    except Exception:
        abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state based on storage id
    """
    state_to_delete = storage.get(State, state_id)
    if state_to_delete is None:
        abort(404)
    storage.delete(state_to_delete)
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Create state object
    """
    try:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        json_data = request.get_json()
        if "name" not in json_data:
            return jsonify({"error": "Missing name"}), 400
        new_state = State(name=json_data["name"])
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing state object based on the id
           Returns:
               A JSON dictionary of the udpated state in a 200 response
               400 response if not dict)
               404 response if the id does not match a storage id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    req.pop("id", None)
    req.pop("created_at", None)
    req.pop("updated_at", None)
    for key, val in req.items():
        setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
