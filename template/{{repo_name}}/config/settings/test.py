# pylint: disable-all

from .local import *  # noqa

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS.remove("debug_toolbar")

TEMPLATE_DEBUG = False
DJANGO_VITE_DEV_MODE = False
DJANGO_VITE_MANIFEST_PATH = DJANGO_VITE_ASSETS_PATH / "manifest.json"
