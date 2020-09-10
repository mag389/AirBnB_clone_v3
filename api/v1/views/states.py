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
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state based on storage id
    """
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


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
        new_object = State(name=json_data["name"])
        new_object.save()
        return jsonify(new_object.to_dict()), 201
    except Exception:
        abort(404)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing state object based on id
           Returns:
               A JSON dictionary of the udpated state in a 200 response
               400 response if not dict)
               404 response if the id does not match an id in storage
    """
    state = storage.get('State', state_id)
    error_message = ""
    if state:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(state, name, value)
            storage.save()
            return jsonify(state.to_dict())
        else:
            error_message = "Not a JSON"
            response = jsonify({'error': error_message})
            response.status_code = 400
            return response

    abort(404)