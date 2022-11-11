import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from .auth_middleware import TokenAuthMiddleware




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_app.settings_folder.settings')
django_asgi = get_asgi_application()

import chat_app.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi,
        "websocket": TokenAuthMiddleware(URLRouter(chat_app.routing.websocket_urlpatterns)),
    }
)
