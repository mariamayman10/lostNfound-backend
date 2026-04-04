from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Missing token"}), 401
        token = auth_header.split(" ")[1]
        try:
            decoded = auth.verify_id_token(token)
            request.user = decoded
        except Exception as e:
            return jsonify({"message": str(e)}), 401
        return f(*args, **kwargs)
    return decorated