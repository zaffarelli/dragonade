from django.urls import re_path
from main.consumers import ParallaxConsumer

websocket_urlpatterns = [
    re_path(r'^ws/socket-server/$', ParallaxConsumer.as_asgi())
]
