"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings.settings')
django_asgi = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi,
        "websocket": URLRouter(chat.routing.websocket_urlpatterns),
    }
)
