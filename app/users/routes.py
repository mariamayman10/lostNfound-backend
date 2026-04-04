from flask import Blueprint, send_from_directory, jsonify
from app.config import Config
from .service import get_user_by_id
import os
users_routes = Blueprint('users', __name__, url_prefix='/users')
@users_routes.route("/profile/<filename>")
def serve_profile_pic(filename):
    os.path.join(Config.PROFILE_UPLOAD_FOLDER, filename)
    return send_from_directory(Config.PROFILE_UPLOAD_FOLDER, filename)

@users_routes.route("/<id>")
def get_user(id):
    try:
        user = get_user_by_id(id)
        print(user)
        return jsonify(user), 200
    except ValueError as e:
        return jsonify({'errorMsg': str(e)}), 401