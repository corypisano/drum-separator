import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute

class User(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = 'Users'
        region = 'us-east-1'
        aws_access_key_id = os.environ["AWS_ACCESS_KEY"]
        aws_secret_access_key = os.environ["AWS_SECRET_KEY"]
    email = UnicodeAttribute(hash_key=True)
    song_count = NumberAttribute(default=0)
    credits = NumberAttribute(default=0)
    ip = UnicodeAttribute(null=True)
    songs = UnicodeSetAttribute(default=[])
    created_at = UTCDateTimeAttribute(null=True)
    last_seen = UTCDateTimeAttribute(null=True)

