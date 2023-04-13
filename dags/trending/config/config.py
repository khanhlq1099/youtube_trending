import boto3
from botocore.client import Config

class MinIO_S3_client:
    s3 = boto3.client('s3',
                    endpoint_url='http://minio:9000',
                    aws_access_key_id='khanhlq10',
                    aws_secret_access_key='khanhlq10',
                    config=Config(signature_version='s3v4')
                    )