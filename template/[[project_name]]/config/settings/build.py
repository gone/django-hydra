# required settings for build command like collectstatic
import os

REQUIRED_KEYS = [
    "SECRET_KEY",
    "DATABASE_URL",
    "DJANGO_ALLOWED_HOSTS",
    "REDIS_URL",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "BUCKET_NAME",
    "AWS_ENDPOINT_URL_S3",
]
for key in REQUIRED_KEYS:
    os.environ[key] = "dummy"
os.environ["SENTRY_DSN"] = "https://dummy@dummy.ingest.sentry.io/1234567"

from .prod import *
