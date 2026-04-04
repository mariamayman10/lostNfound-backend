from flask_marshmallow import Marshmallow
import firebase_admin
from firebase_admin import credentials, firestore, get_app
from app.config import Config

ma = Marshmallow()

def firebase_admin_init():
    try:
        get_app()
    except ValueError:
        cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred)

def get_db():
    return firestore.client()