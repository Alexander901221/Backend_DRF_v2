from django.urls import path
from .views import *

urlpatterns = [
    # Get all ads for map
    path('all', AdListView.as_view()),  # Оптимизированно

    # Create ad
    path('create', AdCreateView.as_view()),  # Оптимизированно

    # Change ad
    path('update/<int:pk>/', AdUpdateView.as_view()),  # Оптимизированно

    # Get ad for pk
    path('ad/<int:pk>/', AdRetrieveAPIView.as_view()),  # Оптимизированно

    # Delete ad for pk
    path('remove/<int:pk>', AdDestroyAPIView.as_view()),  # Оптимизированно

    # Get all my ads
    path('my_ads/', MyAdsListAPIView.as_view()),  # Оптимизированно

    # Notification
    path('notification/', AdView.as_view())
]
