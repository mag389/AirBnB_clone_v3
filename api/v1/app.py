#!/usr/bin/python3
"""Flask blueprint"""
from models import storage
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error):
    """
	Deletes the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(message):
    """
	404 error page in json
    """
    return jsonify({"error": "Not found"}), 404e


if __name__ == '__main__':
	"""
	sets port/host name
	"""
    host = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)