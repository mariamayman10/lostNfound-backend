from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .schema import CommentSchema

comments_routes = Blueprint('comments', __name__)
comments_schema = CommentSchema()
