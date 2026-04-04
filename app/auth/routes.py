from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .schema import RegisterSchema, LoginSchema
from .service import register_service, login_service

auth_routes = Blueprint('auth', __name__, url_prefix='/auth')
register_schema = RegisterSchema()
login_schema = LoginSchema()

@auth_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.form.to_dict()
        resulted_data = register_schema.load(data)
        photo = request.files.get("photo")
        result = register_service(resulted_data, photo)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({
            "errorMsg": "Validation error",
            "errors": e.messages
        }), 400
    except ValueError as e:
        return jsonify({"errorMsg": str(e)}), 401
    except Exception as e:
        return jsonify({"errorMsg": str(e)}), 400

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        resulted_data = login_schema.load(data)
        user_data = login_service(resulted_data)
        return jsonify(user_data), 200
    except ValidationError as e:
        return jsonify({
            "errorMsg": "Validation error",
            "errors": e.messages
        }), 400
    except ValueError as e:
        return jsonify({"errorMsg": str(e)}), 401
    except Exception as e:
        return jsonify({"errorMsg": str(e)}), 400
