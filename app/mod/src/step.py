import os
import time
import shutil
from uuid import uuid1

from app import logging, db
from app.mod.models import TradeDocMaster

logger = logging.getLogger(__name__)


class Step:
    def __init__(self):
        pass

    @staticmethod
    def input_files():
        files_list = list()
        files = os.listdir(os.path.join(os.getcwd(), "shared", "input"))

        for file in files:
            files_list.append(
                {"unique_id": str(uuid1().int), "file_name": file, "status": "pending"}
            )

        db.create_all()
        db.session.add_all(
            [
                TradeDocMaster(
                    unique_id=data_dict.get("unique_id"),
                    file_name=data_dict.get("file_name"),
                    status=data_dict.get("status"),
                )
                for _, data_dict in enumerate(files_list)
            ]
        )
        db.session.commit()

        db_results = TradeDocMaster.query.all()

        return db_results

    @staticmethod
    def run_task(unique_id):
        logger.info(f"Unique ID: {unique_id}")

        os.mkdir(os.path.join(os.getcwd(), "shared", "output", unique_id))

        db_result = TradeDocMaster.query.filter_by(unique_id=unique_id).first()
        file_name = db_result.file_name

        shutil.move(
            os.path.join(os.getcwd(), "shared", "input", file_name),
            os.path.join(os.getcwd(), "shared", "output", unique_id),
        )

        db_result.status = "processing"
        db.session.commit()

        time.sleep(20)

        db_result.status = "processed"
        db.session.commit()
