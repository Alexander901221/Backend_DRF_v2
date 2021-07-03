import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import room_chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest_api_backend_va_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            room_chat.routing.websocket_urlpatterns
        )
    ),
})
