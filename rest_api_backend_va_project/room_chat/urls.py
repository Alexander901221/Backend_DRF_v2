from django.urls import path
from .views import *

urlpatterns = [
    path('', MyRooms.as_view(), name='index'),
    path('messages/<int:pk>/', Messages.as_view(), name='messages'),
]
