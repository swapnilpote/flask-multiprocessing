from uuid import uuid1
from multiprocessing import Process
from flask import Blueprint, render_template
from jinja2 import TemplateNotFound
from werkzeug.exceptions import abort

from app import logging
from app.mod.src.step import Step

logger = logging.getLogger(__name__)


blueprint_aml = Blueprint(
    "aml",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)


@blueprint_aml.route("/", methods=["GET"])
def index():
    try:
        db_results = Step.input_files()
        logger.info(f"Input file data dictionary: \n {'-'*20} \n {db_results}")

        return render_template("index.html", db_results=db_results)
    except TemplateNotFound:
        return abort(404)


@blueprint_aml.route("/start_extraction/<unique_id>", methods=["GET"])
def start_extraction(unique_id):
    try:
        if unique_id:
            pro = Process(target=Step.run_task, args=(unique_id,))
            pro.start()

            return render_template("show_extraction.html", unique_id=unique_id)
    except TemplateNotFound:
        return abort(404)


@blueprint_aml.route("/show_extraction/<unique_id>", methods=["GET"])
def show_extraction(unique_id):
    try:
        if unique_id:
            pass

            return render_template("show_extraction.html", unique_id=unique_id)
    except TemplateNotFound:
        return abort(404)
