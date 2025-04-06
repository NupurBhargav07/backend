from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    age = data.get("age")

    if not all([email, password, name, age]):
        return {"msg": "All fields (name, email, password, age) are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"msg": "Email already exists"}, 400

    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw, name=name, age=age)
    db.session.add(user)
    db.session.commit()

    return {"msg": "Registered successfully"}


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if user and check_password_hash(user.password, data.get("password")):
        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}
    return {"msg": "Invalid credentials"}, 401
