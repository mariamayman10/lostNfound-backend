import datetime
from string import Template
from app.comments.schema import CommentSchema
from app.extensions import get_db

comments_schema = CommentSchema()

reply_str = "$name replied to your comment on $title report"
reply_obj = Template(reply_str)
comment_str = "$name commented on your $title report"
comment_obj = Template(comment_str)

def create_notifications(user_data, comment_data, report_data, parent_data, user_id):
    db = get_db()
    if parent_data and parent_data["userId"] != user_id:
        db.collection("users") \
          .document(parent_data["userId"]) \
          .collection("notifications") \
          .add({
              "message": reply_obj.substitute(
                  name=user_data["name"],
                  title=report_data["title"]
              ),
              "userId": parent_data["userId"],
              "seen": False,
              "created_at": datetime.datetime.now(),
              "type": "reply",
              "reportId": comment_data["reportId"]
          })

    elif report_data["userId"] != user_id:
        db.collection("users") \
          .document(report_data["userId"]) \
          .collection("notifications") \
          .add({
              "message": comment_obj.substitute(
                  name=user_data["name"],
                  title=report_data["title"]
              ),
              "userId": report_data["userId"],
              "seen": False,
              "created_at": datetime.datetime.now(),
              "type": "comment",
              "reportId": comment_data["reportId"]
          })


def create_comment_service(comment_data, user_id):
    db = get_db()
    report = db.collection("reports").document(comment_data["reportId"]).get()
    if not report.exists:
        raise ValueError("Report not found")
    report_data = report.to_dict()
    if report_data["status"] == "closed":
        raise ValueError("Report closed")

    parent_data = None
    if comment_data["parentId"]:
        parent = db.collection("comments").document(comment_data["parentId"]).get()

        if not parent.exists:
            raise ValueError("Parent comment not found")

        parent_data = parent.to_dict()

        if parent_data["reportId"] != comment_data["reportId"]:
            raise ValueError("Invalid parent comment")

        if parent_data.get("parentId"):
            raise ValueError("Cannot reply to a reply")

    doc_ref = db.collection("comments").document()
    comment = {
        "userId": user_id,
        "content": comment_data["content"],
        "reportId": comment_data["reportId"],
        "parentId": comment_data["parentId"],
        "createdAt": datetime.datetime.now(),
    }
    doc_ref.set(comment)

    user = db.collection("users").document(user_id).get()
    user_data = user.to_dict()
    comment["userName"] = user_data["name"]

    create_notifications(user_data, comment_data, report_data, parent_data, user_id)
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