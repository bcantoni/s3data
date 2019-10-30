import boto3
from botocore.exceptions import ClientError
import json


class S3Data:
    def __init__(self, aws_access_key, aws_secret_access_key, bucket):
        """Initialize S3 connection given access/secret keys"""
        self.s3 = boto3.resource("s3",
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_access_key)
        self.bucket = bucket

    def put(self, key, data):
        """Put data to specified key in S3 bucket"""
        self.s3.Bucket(self.bucket).Object(key=key).put(Body=json.dumps(data))

    def get(self, key):
        """Get data from specified key in S3 bucket"""
        try:
            json_data = self.s3.Bucket(self.bucket).Object(key=key).get()["Body"]
            data = json.load(json_data)
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return dict()
            else:
                raise

        return data

    def delete(self, key):
        """Delete key from S3 bucket"""
        self.s3.Bucket(self.bucket).Object(key=key).delete()
