import datetime, os
from app import Config
from app.extensions import get_db
from app.globalHelpers import save_image, move_file
from .schema import ReportSchema, GetReportSchema
from google.cloud.firestore_v1 import Increment

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
