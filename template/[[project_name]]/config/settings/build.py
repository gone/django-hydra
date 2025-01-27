# required settings for build command like collectstatic
import os
REQUIRED_KEYS = ['DJANGO_SECRET_KEY', "DATABASE_URL", "DJANGO_ALLOWED_HOSTS", "REDIS_URL",
                 "DJANGO_AWS_ACCESS_KEY_ID", "DJANGO_AWS_SECRET_ACCESS_KEY",
                 "DJANGO_AWS_STORAGE_BUCKET_NAME", "DJANGO_AWS_S3_ENDPOINT_URL"
                 ]
for key in REQUIRED_KEYS:
    os.environ[key] = 'dummy'
os.environ['SENTRY_DSN'] = 'https://dummy@dummy.ingest.sentry.io/1234567'

from .prod import *
