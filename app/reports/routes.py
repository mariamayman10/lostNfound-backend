from flask import Blueprint, request, jsonify, send_from_directory
from marshmallow import ValidationError
from .schema import ReportSchema, CreateReportSchema, UpdateReportSchema
from .service import get_report_service, get_reports_service, create_report_service, get_my_reports_service, update_report_service
from ..auth.decorators import require_auth
from app.config import Config
import os

reports_routes = Blueprint('reports', __name__, url_prefix='/reports')
report_schema = ReportSchema()
create_report_schema = CreateReportSchema()
update_report_schema = UpdateReportSchema()

@reports_routes.route('/', methods=['GET'])
def get_reports():
    try:
        params = request.args.to_dict()
        reports = get_reports_service(params)
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({'errorMsg': str(e)}), 400

@reports_routes.route('/create', methods=['POST'])
@require_auth
def create_report():
    try:
        data = request.form.to_dict()
        resulted_data = create_report_schema.load(data)
        user_id = request.user["uid"] # type: ignore
        images = request.files.getlist('images')
        result = create_report_service(resulted_data, images, user_id)
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


@reports_routes.route('/<id>', methods=['PUT'])
@require_auth
def update_report(id):
    try:
        user_id = request.user["uid"]  # type: ignore
        data = update_report_schema.load(request.json)
        report = update_report_service(id, data, user_id)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"errorMsg": str(e)}), 400
    except ValidationError as e:
        return jsonify({
            "errorMsg": "Validation error",
            "errors": e.messages
        }), 400


@reports_routes.route('/<id>', methods=['GET'])
@require_auth
def get_report(id):
    try:
        user_id = request.user["uid"]  # type: ignore
        report = get_report_service(id, user_id)
        return jsonify(report), 200
    except ValueError as e:
        return jsonify({'errorMsg': str(e)}), 401

@reports_routes.route("/my")
@require_auth
def get_my_reports():
    try:
        user_id = request.user["uid"]  # type: ignore
        reports = get_my_reports_service(user_id)
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({'errorMsg': str(e)}), 400



@reports_routes.route("/report-img/<filename>")
def server_report_img(filename):
    os.path.join(Config.REPORTS_UPLOAD_FOLDER, filename)
    return send_from_directory(Config.REPORTS_UPLOAD_FOLDER, filename)