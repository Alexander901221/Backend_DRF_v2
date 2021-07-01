from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rest Framework path
    path('api-auth/', include('rest_framework.urls')),

    # User
    path('api/users/', include('user.urls')),

    # Ad
    path('api/ad/', include('ad.urls')),

    # Bid
    path('api/bid/', include('bid.urls')),

    # Participant
    path('api/participant/', include('participant.urls')),

    # Room chat
    path('api/room_chat/', include('room_chat.urls')),

    # Token
    path('api/token/', TokenObtainPairView.as_view()),  # для авторизации {username: 'alex123', password: '123qwe'}
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
