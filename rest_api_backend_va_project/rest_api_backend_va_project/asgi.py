import os

from channels.auth import AuthMiddlewareStack
from room_chat.chatmiddleware import JwtAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# import room_chat.routing
from room_chat.consumers import ChatConsumer
from user.consumers import NoseyConsumer
from ad.consumers import AdConsumer
from bid.consumers import BidConsumer
from django.urls import path, re_path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest_api_backend_va_project.settings")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
			URLRouter([
					path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
                    path('ws/notification/user/<int:user>/', NoseyConsumer.as_asgi()),
                    path('ws/notification/ad/<int:city>/', AdConsumer.as_asgi()),
                    path('ws/notification/bid/<int:ad>/', BidConsumer.as_asgi())
			])
    ),
})
