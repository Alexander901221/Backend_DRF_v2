from django.urls import path
from .views import *

urlpatterns = [
    # Create participant
    path('create', ParticipantCreateView.as_view()),

    # Get participant for pk
    path('<int:ad_pk>/<int:participant_pk>/', ParticipantRetrieveAPIView.as_view()),  # Оптимизированно

    # Get my participants for ad
    path('my_participants/<int:pk>/', MyParticipantsListAPIView.as_view()),  # Оптимизированно

    # Delete participant
    path('remove/<int:ad_pk>/<participant_pk>/', ParticipantDestroyAPIView.as_view())  # Оптимизированно
]
