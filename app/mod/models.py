from enum import unique
from app import db


class TradeDocMaster(db.Model):
    __tablename__ = "trade_doc_master"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    unique_id = db.Column(db.String, unique=True, nullable=False)
    file_name = db.Column(db.String, unique=False, nullable=True)
    status = db.Column(db.String, unique=False, nullable=True)
