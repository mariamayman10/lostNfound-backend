import datetime

from app.comments.schema import CommentSchema
from app.extensions import get_db

comments_schema = CommentSchema()


def create_comment_service(comment_data, user_id):
    report = get_db().collection("reports").document(comment_data["reportId"]).get()
    if not report.exists:
        raise ValueError("Report not found")
    if comment_data["parentId"]:
        parent = get_db().collection("comments").document(comment_data["parentId"]).get()
        if not parent.exists:
            raise ValueError("Parent comment not found")

        parent_data = parent.to_dict()
        if parent_data["reportId"] != comment_data["reportId"]:
            raise ValueError("Invalid parent comment")
        if parent_data.get("parentId"):
            raise ValueError("Cannot reply to a reply")

    doc_ref = get_db().collection("comments").document()
    comment = {
        "userId": user_id,
        "content": comment_data["content"],
        "reportId": comment_data["reportId"],
        "parentId": comment_data["parentId"],
        "createdAt": datetime.datetime.now(),
    }
    doc_ref.set(comment)
    user = get_db().collection("users").document(user_id).get()
    user_data = user.to_dict()
    comment["userName"] = user_data["name"]
    return comments_schema.dump(comment)

def get_report_comments(report_id):
    docs = get_db().collection("comments").where("reportId", "==", report_id).stream()

    comments = []
    for doc in docs:
        data = doc.to_dict()
        user = get_db().collection("users").document(data["userId"]).get()
        user_data = user.to_dict()
        data["id"] = doc.id
        data["userName"] = user_data["name"]
        comments.append(data)
    return comments