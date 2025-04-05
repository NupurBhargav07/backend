from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, User, Question, Option, Answer, QuestionFlow

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

    admin = Admin(app, name='Questionnaire Admin', template_mode='bootstrap4')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Question, db.session))
    admin.add_view(ModelView(Option, db.session))
    admin.add_view(ModelView(Answer, db.session))
    admin.add_view(ModelView(QuestionFlow, db.session))

    from .auth import auth_bp
    from .questionnaire import questionnaire_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(questionnaire_bp)

    return app
