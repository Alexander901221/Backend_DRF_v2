import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# import room_chat.routing
from room_chat.consumers import ChatConsumer
from notification.consumers import NoseyConsumer
from django.urls import path, re_path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest_api_backend_va_project.settings")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
			URLRouter([
					path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
                    path('ws/notification/', NoseyConsumer.as_asgi())
			])
    ),
})
