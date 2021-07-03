from django.urls import path
from .views import *

urlpatterns = [
    path('', MyRooms.as_view(), name='index'),
    path('messages/<int:pk>/', Messages.as_view(), name='messages'),

    path('<str:room_name>/', room, name='room'),
    # path('my_rooms/', MyRoomsListAPIView.as_view()),
]
