from django.urls import path
from .views import *

urlpatterns = [
    # Get all bids
    path('all', BidListView.as_view()),  # Оптимизированно

    # Get bid for pk
    path('bid/<int:pk>/', BidRetrieveAPIView.as_view()),  # Оптимизированно

    # Create bid
    path('create', BidCreateView.as_view()),

    # Update bid for pk
    path('update/<int:pk>/', BidUpdateView.as_view()),

    # Delete bid for pk
    path('remove/<int:pk>/', BidRejected.as_view()),  # Оптимизированно

    # Receiving all my applications
    path('my_bids/', MyBidsListAPIView.as_view())  # Оптимизированно
]
