from app.extensions import get_db
from .schema import UserSchema

user_schema = UserSchema()

def get_user_by_id(user_id):
    doc = get_db().collection('users').document(user_id).get()
    if not doc.exists:
        return "User not found"
    user = doc.to_dict()
    return user_schema.dump(user)