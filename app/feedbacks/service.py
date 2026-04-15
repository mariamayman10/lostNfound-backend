from app.extensions import get_db
from google.cloud import firestore
import datetime

def create_feedback_service(feedback, user_id):
    try:
        user = get_db().collection('users').document(user_id).get()
        if not user.exists:
            raise ValueError('User not found')
        doc_ref = get_db().collection('feedbacks').document()
        doc_ref.set({
            'message': feedback["message"],
            'rating': feedback["rating"],
            'createdAt': datetime.datetime.now(),
            'user_id': user_id,
        })
        feedback_id = doc_ref.id
        return feedback, feedback_id
    except Exception as e:
        raise Exception('Failed to create feedback')

def get_feedbacks_service(params):
    try:
        docs = get_db().collection("feedbacks").order_by("createdAt", direction=firestore.Query.DESCENDING).limit(int(params["limit"])).stream()
        feedbacks = []
        user_cache = {}

        for doc in docs:
            data = doc.to_dict()
            user_id = data.get("user_id")
            if user_id not in user_cache:
                user_doc = get_db().collection("users").document(user_id).get()
                if user_doc.exists:
                    user_cache[user_id] = user_doc.to_dict()
                else:
                    user_cache[user_id] = {
                        "name": "Unknown",
                        "photoUrl": None
                    }

            user = user_cache[user_id]

            feedbacks.append({
                "id": doc.id,
                "message": data.get("message"),
                "rating": data.get("rating"),
                "createdAt": data.get("createdAt"),
                "user": {
                    "name": user.get("name"),
                    "photoUrl": user.get("photoUrl")
                }
            })

        return feedbacks

    except Exception as e:
        print("ERROR:", e)
        raise Exception("Failed to fetch feedbacks")