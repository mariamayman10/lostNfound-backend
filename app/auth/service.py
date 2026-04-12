import datetime, os, requests
from firebase_admin import auth
from .schema import UserSchema
from .helpers import send_email
from app.globalHelpers import save_image, move_file
from app.config import Config
from app.extensions import get_db



user_schema = UserSchema()

def prepare_email(user):
    link = auth.generate_email_verification_link(
        user.email,
        action_code_settings=auth.ActionCodeSettings(
            url=f"{Config.FRONTEND_URL}/verify?uid={user.uid}",
            handle_code_in_app = False
        )
    )
    send_email(user.email, link)

def save_user(user_data):
    user = auth.create_user(
        email=user_data['email'],
        password=user_data['password']
    )
    prepare_email(user)
    firebase_user = {
        "name": user_data['name'],
        "email": user_data['email'],
        "phoneNumber": user_data['phoneNumber'],
        "photoUrl": None,
        "postsCount": 0,
        "createdAt": datetime.datetime.now(),
        "uid": user.uid
    }
    get_db().collection('users').document(user.uid).set(firebase_user)
    return firebase_user, user.uid

def register_service(user_data, profile_picture):
    temp_filepath = None
    try:
        temp_filepath = save_image(profile_picture, Config.TEMP_UPLOAD_FOLDER)

        firebase_user, user_uid = save_user(user_data)
        img_url = move_file(temp_filepath, Config.PROFILE_UPLOAD_FOLDER)
        get_db().collection('users').document(user_uid).update({
            "photoUrl": img_url
        })
        firebase_user['photoUrl'] = img_url
        return user_schema.dump(firebase_user)

    except Exception as e:
        if temp_filepath and os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        raise e

def login_service(login_data):
    payload = {
        "email": login_data.get('email'),
        "password": login_data.get('password'),
        "returnSecureToken": True
    }

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={Config.FIREBASE_API_KEY}"
    res = requests.post(url, json=payload)
    data = res.json()
    if "error" in data:
        raise ValueError(data["error"]["message"])
    id_token = data["idToken"]
    firebase_uid = data["localId"]

    lookup_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={Config.FIREBASE_API_KEY}"
    lookup_res = requests.post(lookup_url, json={"idToken": id_token}).json()
    email_verified = lookup_res["users"][0]["emailVerified"]
    if not email_verified:
        raise ValueError("Email not verified. Please check your inbox.")

    user_doc = get_db().collection("users").document(firebase_uid).get()
    if not user_doc.exists:
        raise ValueError("User record not found in Firestore")
    user_data = user_doc.to_dict()
    return {
        "idToken": id_token,
        "refreshToken": data["refreshToken"],
        "expiresIn": data["expiresIn"],
        "userId": firebase_uid,
        "name": user_data['name'],
        "email": user_data['email'],
        "phoneNumber": user_data['phoneNumber'],
        "photoUrl": user_data['photoUrl'],
        "postsCount": user_data['postsCount'],
        "createdAt": user_data['createdAt']
    }
