"""
ASGI config for quizapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from uvicorn.workers import UvicornWorker as BaseUvicornWorker

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizapp.settings')

application = get_asgi_application()

class UvicornWorker(BaseUvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools", "lifespan": "off"}