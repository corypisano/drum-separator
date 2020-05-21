import logging
import os

from flask import render_template, Blueprint, request, current_app

from app.utils import allowed_file
from app.file_manager import save_file, upload_file_to_s3

api = Blueprint("api", __name__)

logger = logging.getLogger()

import boto3

# Create SQS client
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

queue_url = "https://sqs.us-east-1.amazonaws.com/797520980319/break-up-song-queue"


@api.route("/", methods=["GET"])
def home():
    """TODO:
    if logged in, render template without email
    """
    return render_template("home.html")


@api.route("/check", methods=["GET"])
def check():
    return {"message": "check"}, 200


@api.route("/process", methods=["POST"])
def process():
    logger.info("in POST /process")

    if "file" not in request.files:
        logger.info("no file in request")
        return "no file yo", 400
    f = request.files["file"]
    if not allowed_file(f.filename):
        logger.info("file not an allowed file type")
        return "nah, file not allowed", 400

    email = request.form.get("email")
    print("email is ", email)

    # save input file and separate
    input_filepath, safe_filename = save_file(f)
    song_name = safe_filename.split(".")[0]

    signed_input_url = upload_file_to_s3(input_filepath, object_name=safe_filename)
    print("signed_input_url is", signed_input_url)
    print("sending sqs message")
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes={
            "file_s3_url": {"DataType": "String", "StringValue": signed_input_url},
            "email": {"DataType": "String", "StringValue": email,},
            "song_name": {"DataType": "String", "StringValue": song_name,},
        },
        MessageBody="body",
    )
    return "ok", 200
