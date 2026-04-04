from flask import Blueprint, send_from_directory, jsonify
users_routes = Blueprint('users', __name__, url_prefix='/users')
