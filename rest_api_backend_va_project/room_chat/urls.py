from django.urls import path
from .views import *

urlpatterns = [
    # Create participant
    path('all', RoomListView.as_view()),
]
