# pylint: disable-all

"""
ASGI config for asgi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Import websocket application here, so apps from django_application are loaded first
from {{cookiecutter.repo_name}}.config.websocket import websocket_application  # noqa isort:skip

# fmt: off
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "{{cookiecutter.repo_name}}.config.settings.prod",
)
# fmt: on

django_application = get_asgi_application()
# Apply ASGI middleware here.


async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
