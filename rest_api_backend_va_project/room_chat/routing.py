from django.urls import re_path

from . import consumers

websocket_urlpatterns = [  # Адрес по которому будут отправлятся socket
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
