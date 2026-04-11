import datetime, os
from app import Config
from app.extensions import get_db
from app.globalHelpers import save_image, move_file
from .schema import ReportSchema, GetReportSchema
from ..users.service import get_user_by_id
from ..comments.service import get_report_comments
from google.cloud.firestore_v1 import Increment
from google.cloud import firestore

report_schema = ReportSchema()
get_report_schema = GetReportSchema()


def save_report(report, user_id):
    report = {
        "title": report['title'],
        "description": report['description'],
        "location": report['location'],
        "category": report['category'],
        "status": "open",
        "type": report['type'],
        "imageUrls": [],
        "userId": user_id,
        "createdAt": datetime.datetime.now()
    }
    doc_ref = get_db().collection('reports').document()
    doc_ref.set(report)
    report_id = doc_ref.id
    return report, report_id

def create_report_service(report, images, user_id):
    if len(images) < 1 or len(images) > 3:
        raise ValueError("You must upload between 1 and 3 images")
    temp_filepaths = []
    try:
        for image in images:
            temp_filepaths.append(save_image(image, Config.TEMP_UPLOAD_FOLDER))

        firebase_report, report_id = save_report(report, user_id)
        image_urls = []
        for temp_filepath in temp_filepaths:
            image_urls.append(move_file(temp_filepath, Config.REPORTS_UPLOAD_FOLDER))
        get_db().collection('reports').document(report_id).update({
            "imageUrls": image_urls
        })
        get_db().collection("users").document(user_id).update({
            "postsCount": Increment(1)
        })
        firebase_report['imageUrls'] = image_urls
        return report_schema.dump(firebase_report)

    except Exception as e:
        for temp_filepath in temp_filepaths:
            if temp_filepaths and os.path.exists(temp_filepath):
                os.remove(temp_filepath)
        raise e

def get_report_service(report_id, uid):
    doc = get_db().collection('reports').document(report_id).get()
    if not doc.exists:
        raise ValueError("Report not found")
    report = doc.to_dict()
    report['id'] = doc.id
    report['userName'] = get_user_by_id(report.get('userId'))["name"]
    report['isOwner'] = report["userId"] == uid
    report['comments'] = get_report_comments(report_id)
    return report

def get_reports_service(params):
    print(params)
    query = get_db().collection("reports")
    if "type" in params:
        query = query.where("type", "==", params["type"])
    if "status" in params:
        query = query.where("status", "==", params["status"])
    if "sortby" in params:
        if params["sortby"] == "asc":
            order = firestore.Query.ASCENDING
        else:
            order = firestore.Query.DESCENDING
        query = query.order_by("createdAt", direction=order)
    category_filter = params.get("category", "").lower()
    location_filter = params.get("location", "").lower()
    title_filter = params.get("title", "").lower()

    docs = query.stream()
    reports = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        title = data.get("title", "").lower()
        location = data.get("location", "").lower()
        category = data.get("category", "").lower()
        if category_filter and category_filter not in category:
            continue
        if title_filter and title_filter not in title:
            continue
        if location_filter and location_filter not in location:
            continue
        reports.append(data)

    return get_report_schema.dump(reports, many=True)

def get_my_reports_service(user_id):
    docs = get_db().collection("reports").where("userId", "==", user_id).stream()
    my_reports = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        my_reports.append(data)
    return get_report_schema.dump(my_reports, many=True)

def update_report_service(report_id, data, user_id):
    doc = get_db().collection("reports").document(report_id).get()
    if not doc.exists:
        raise Exception("Report not found")
    if doc.to_dict()["userId"] != user_id:
        raise Exception("You are not the owner of the report")
    if doc.to_dict()["status"] == "closed":
        raise Exception("Report is closed")
    get_db().collection("reports").document(report_id).update(data)
    report = get_db().collection("reports").document(report_id).get().to_dict()
    return report_schema.dump(report)
