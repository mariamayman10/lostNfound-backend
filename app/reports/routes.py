from flask import Blueprint, request, jsonify, send_from_directory
from marshmallow import ValidationError
from .schema import ReportSchema, CreateReportSchema, UpdateReportSchema
import os

reports_routes = Blueprint('reports', __name__, url_prefix='/reports')
report_schema = ReportSchema()
create_report_schema = CreateReportSchema()
update_report_schema = UpdateReportSchema()
@reports_routes.route('/', methods=['GET'])
def get_reports():
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

@reports_routes.route('/<id>', methods=['GET'])
@require_auth
def get_report(id):

@reports_routes.route("/my")
@require_auth
def get_my_reports():

@reports_routes.route("/report-img/<filename>")
def server_report_img(filename):
