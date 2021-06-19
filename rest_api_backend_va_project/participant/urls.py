from django.urls import path
from .views import *

urlpatterns = [
    path('all', ParticipantListView.as_view()),
    path('create', ParticipantCreateView.as_view()),
    path('participant/<int:pk>/', ParticipantRetrieveAPIView.as_view()),
    path('my_participants/', MyParticipantsListAPIView.as_view()),
    path('remove/<int:pk>/', ParticipantDestroyAPIView.as_view())
]
