from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'lobby/(?P<chat_title>\w+)/$', consumers.ChatConsumer.as_asgi()),
]