import os
import logging

from flask import current_app
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename

AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
s3_client = boto3.client(
    "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
)

# create directory to store uploaded files
INPUT_FILE_DIR = "./input_files"
os.makedirs(INPUT_FILE_DIR, exist_ok=True)

logger = logging.getLogger()


def save_file(input_file):
    """Saves file to tmp directory"""
    safe_filename = secure_filename(input_file.filename)
    filepath = os.path.join(INPUT_FILE_DIR, safe_filename)

    logger.info(f"saving file to {filepath}")
    input_file.save(filepath)
    return filepath, safe_filename


def upload_file_to_s3(file_name, object_name=None, bucket_name="drum-separator"):
    """Upload a file to an S3 bucket, return signed url

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :param bucket_name: Bucket to upload to
    :return: signed_url to access the file
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        logger.info(f"uploading file: {file_name}")
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return None

    signed_url = get_presigned_url(bucket_name, object_name)
    return signed_url


def get_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
