import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    DEBUG = os.getenv("FLASK_DEBUG", True)
    TESTING = os.getenv("FLASK_TESTING", False)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    TEMP_UPLOAD_FOLDER = os.getenv("TEMP_UPLOAD_FOLDER", "uploads/temp")
    PROFILE_UPLOAD_FOLDER = os.getenv("PROFILE_UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads", "profilePics"))
    REPORTS_UPLOAD_FOLDER = os.getenv("REPORTS_UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads", "reports"))
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS",
                                     "secrets/firebase_credentials.json")
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "AIzaSyBgf3RF6Jg_iCeylRTAS4w8wTSf7dKTjeU")
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = os.getenv("EMAIL_PORT", "465")
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "lostnfound7985@gmail.com")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")