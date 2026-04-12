from flask import Flask
from flask_cors import CORS

from .extensions import ma, firebase_admin_init
from .config import Config
from .auth.routes import auth_routes
from .reports.routes import reports_routes
from .users.routes import users_routes
from .comments.routes import comments_routes
from .feedbacks.routes import feedback_routes
import os

def create_app():
  app = Flask(__name__)
  app.config.from_object("app.config.Config")
  CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
  ma.init_app(app)
  firebase_admin_init()

  upload_folders = [
    Config.UPLOAD_FOLDER,
    Config.TEMP_UPLOAD_FOLDER,
    Config.PROFILE_UPLOAD_FOLDER,
    Config.REPORTS_UPLOAD_FOLDER
  ]

  for folder in upload_folders:
    os.makedirs(folder, exist_ok=True)

  app.register_blueprint(auth_routes)
  app.register_blueprint(reports_routes)
  app.register_blueprint(users_routes)
  app.register_blueprint(comments_routes)
  app.register_blueprint(feedback_routes)

  return app