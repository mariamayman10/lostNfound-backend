from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .schema import CreateFeedback
from .service import create_feedback_service, get_feedbacks_service
from ..auth.decorators import require_auth

feedback_routes = Blueprint('feedback', __name__, url_prefix='/feedback')
create_feedback_schema = CreateFeedback()

@feedback_routes.route('', methods=['POST'])
@require_auth
def create_feedback():
    try:
        data = request.json
        user_id = request.user["uid"]  # type: ignore
        resulted_data = create_feedback_schema.load(data)
        result = create_feedback_service(resulted_data, user_id)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({
            "errorMsg": "Validation error",
            "errors": e.messages
        }), 400

@feedback_routes.route('', methods=['GET'])
def get_feedbacks():
    try:
        feedbacks = get_feedbacks_service()
        return jsonify(feedbacks), 200
    except Exception as e:
        return jsonify({
            "errorMsg": "Retrieving error",
        }), 400