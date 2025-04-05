from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    return app
