from flask import Blueprint, request, jsonify, send_from_directory
from marshmallow import ValidationError
from .schema import ReportSchema, CreateReportSchema, UpdateReportSchema
import os

reports_routes = Blueprint('reports', __name__, url_prefix='/reports')
report_schema = ReportSchema()
create_report_schema = CreateReportSchema()
update_report_schema = UpdateReportSchema()
