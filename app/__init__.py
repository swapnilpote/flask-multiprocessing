import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

if app.config.get("ENV") == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config.get("ENV") == "testing":
    app.config.from_object("config.TestingConfig")
elif app.config.get("ENV") == "development":
    app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)

from app.mod.views import blueprint_aml

app.register_blueprint(blueprint_aml, url_prefix="/")
