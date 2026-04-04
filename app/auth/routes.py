from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .schema import RegisterSchema, LoginSchema

auth_routes = Blueprint('auth', __name__, url_prefix='/auth')
register_schema = RegisterSchema()
login_schema = LoginSchema()
