# chat/routing.py
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>', consumers.ChatConsumer.as_asgi()),
]