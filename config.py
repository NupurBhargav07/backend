import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "a4ebc81f58ef958733e9b89c37940b1bc042f2e555ea5a655b94cece4f59936f")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "a4ebc81f58ef958733e9b89c37940b1bc042f2e555ea5a655b94cece4f59936f")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
