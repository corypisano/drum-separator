import logging
import os

from flask import render_template, Blueprint, request, current_app

from app.utils import allowed_file
from app.file_manager import FileManager
from app.queue_manager import QueueManager

api = Blueprint("api", __name__)

logger = logging.getLogger()


@api.route("/", methods=["GET"])
def home():
    """TODO:
    if logged in, render template without email
    """
    return render_template("home.html")


@api.route("/example", methods=["GET"])
def example():
    """Example samples with audio player"""
    return render_template("example.html")


@api.route("/check", methods=["GET"])
def check():
    return {"message": "check"}, 200


@api.route("/process", methods=["POST"])
def process():
    logger.info("in POST /process")

    email = request.form.get("email")
    if "file" not in request.files:
        logger.info("no file in request")
        return "no file yo", 400
    f = request.files["file"]
    if not allowed_file(f.filename):
        logger.info("file not an allowed file type")
        return "nah, file not allowed", 400

    # save input file and separate
    input_filepath, safe_filename = FileManager.save_file(f)
    song_name = safe_filename.split(".")[0]

    s3_object_name = FileManager.upload_to_s3(input_filepath, object_name=safe_filename)
    data = {"s3_object_name": s3_object_name, "email": email, "song_name": song_name}
    response = QueueManager.send_message("break_up_drums", data)
    return "ok", 200


@api.route("/process_error", methods=["POST"])
def handle_process_error():
    """This app should be responsible for managing dynamodb store
    so CRUD actions can be done by client
    but if we update someones credits and then the process fails,
    need an endpoint for the worker to hit so that the credit isn't taken away
    """
    # email
    # error?
    # restore_credit = true/false
    pass
