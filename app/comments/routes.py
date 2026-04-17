from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.auth.decorators import require_auth
from .schema import CommentSchema
from .service import create_comment_service

comments_routes = Blueprint('comments', __name__)
comments_schema = CommentSchema()

@comments_routes.route('/comments', methods=['POST'])
@require_auth
def create_comment():
    try:
        user_id = request.user["uid"]  # type: ignore
        comment_data = comments_schema.load(request.json)
        comment = create_comment_service(comment_data, user_id)
        return jsonify(comment), 201
    except ValueError as e:
        return jsonify({'errorMsg': str(e)}), 400
    except ValidationError as e:
        return jsonify({
            "errorMsg": "Validation error",
            "errors": e.messages
        }), 400

