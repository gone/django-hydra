# pylint: disable-all
import json
from os import environ as env

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

aws_access_key_id = env["DJANGO_AWS_ACCESS_KEY_ID"]
aws_secret_access_key = env["DJANGO_AWS_SECRET_ACCESS_KEY"]
endpoint_url = env["DJANGO_AWS_S3_ENDPOINT_URL"]
bucketname = env["DJANGO_AWS_STORAGE_BUCKET_NAME"]
api_port = ":9000"

s3 = boto3.client(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": f"arn:aws:s3:::{bucketname}/*",
        },
    ],
}
bucket_policy = json.dumps(bucket_policy)


def delete_bucket():
    s3_resource = boto3.resource(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )
    bucket = s3_resource.Bucket(bucketname)
    for obj in bucket.objects.all():
        obj.delete()
    bucket.delete()


def create_bucket():
    try:
        s3.head_bucket(Bucket=bucketname)
        print(f"bucket {bucketname} exists!")
    except ClientError:
        print(f"creating bucket {bucketname}")
        try:
            s3.create_bucket(Bucket=bucketname)
            s3.put_bucket_policy(Bucket=bucketname, Policy=bucket_policy)
        except ClientError as e:
            print("Unable to contact minio")
            print(e)


if __name__ == "__main__":
    create_bucket()
