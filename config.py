import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = False
    CRRF_ENABLED = True
    SECRET = os.environ.get("SECRET")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    # NETWORK_FOLDER = os.path.join(os.getcwd(), "shared")


class DevelopmentConfig:
    DEBUG = True
    # Load sql database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    TESTING = True
    DEBUG = True


class ProductionConfig:
    DEBUG = False
    TESTING = False
