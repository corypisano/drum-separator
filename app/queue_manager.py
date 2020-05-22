import os
import json

import boto3

# Create SQS client
SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]

sqs = boto3.client(
    "sqs",
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)


class QueueManager:
    """Manages SQS queue"""

    def send_message(message_type, data):
        print(f"sending sqs message. message_type={message_type}, data={data}")
        message_body = json.dumps({"message_type": message_type, "data": data})

        response = sqs.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=message_body,)
        return response
