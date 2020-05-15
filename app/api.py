import logging

from flask import render_template, Blueprint, jsonify, request, current_app

from app.audio_separator import separate_drums
from app.utils import allowed_file
from app.file_manager import save_file, upload_file_to_s3

api = Blueprint("api", __name__)

logger = logging.getLogger()


@api.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@api.route("/check", methods=["GET"])
def check():
    return jsonify({"message": "check"}), 200


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

    # save input file and separate
    input_filepath = save_file(f)

    logger.info("separating drums")
    output_dir = "./output_files"  # change to file manager type (create dir safely)
    separate_drums(input_filepath, output_dir)

    # upload separated tracks to S3 and return URL's
    signed_input_url = upload_file_to_s3(input_filepath, object_name=f.filename)
    output_path = f"{output_dir}/NewYorican/drums.wav"
    signed_drum_url = upload_file_to_s3(output_path, object_name='drums.wav')
    logger.info("done, returning JSON response")
    response = {
        "success": True,
        "drum_link": signed_drum_url,
        "audio_link": "https://audio.com",
    }
    return jsonify(response), 200
