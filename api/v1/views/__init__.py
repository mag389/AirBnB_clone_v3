#!/usr/bin/python3
"""Blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if app_views:
    from api.v1.views.index import *
    try:
        import api.v1.views.amenities
    except ImportError as error:
        pass
    try:
        import api.v1.views.states
    except ImportError as error:
        pass
    try:
        import api.v1.views.cities
    except ImportError as error:
        pass
    try:
        import api.v1.views.users
    except ImportError as error:
        pass
    try:
        import api.v1.views.places
    except ImportError as error:
        pass
    try:
        import api.v1.views.places_reviews
    except ImportError as error:
        pass
    """
    from api.v1.views.places_amenities import *
    from api.v1.app import *
    """
