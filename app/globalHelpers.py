import os, uuid, shutil
from flask import request
from firebase_admin import auth

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image, folder):
    if image is None:
        raise ValueError("No image provided")
    if not allowed_file(image.filename):
        raise ValueError("Invalid image provided, only png, jpg, and jpeg supported")
    ext = image.filename.rsplit('.', 1)[1].lower()
    filename = f'{uuid.uuid4().hex}.{ext}'
    filepath = os.path.join(folder, filename)
    image.save(filepath)
    return filepath

def move_file(temp_path, folder):
    ext = temp_path.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    final_path = os.path.join(folder, filename)
    shutil.move(temp_path, final_path)

    if folder.endswith("profilePics"):
        return f"/uploads/profilePics/{filename}"
    elif folder.endswith("reports"):
        return f"/uploads/reports/{filename}"
    else:
        return f"/uploads/{filename}"

def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise ValueError("Missing token")

    token = auth_header.split(" ")[1]
    decoded_token = auth.verify_id_token(token)

    return decoded_token["uid"]