from django.urls import path
from .views import *

urlpatterns = [
    # Get all participants
    path('all', ParticipantListView.as_view()),

    # Create participant
    path('create', ParticipantCreateView.as_view()),

    # Get participant for pk
    path('participant/<int:pk>/', ParticipantRetrieveAPIView.as_view()),

    # Get my participants for ad
    path('my_participants/', MyParticipantsListAPIView.as_view()),  # Оптимизированно

    # Delete participant
    path('remove/<int:pk>/', ParticipantDestroyAPIView.as_view())
]
