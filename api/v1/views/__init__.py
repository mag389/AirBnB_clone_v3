#!/usr/bin/python3
"""views init file"""
from models import storage
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv

app_views
