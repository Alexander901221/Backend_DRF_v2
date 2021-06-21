from django.urls import path
from .views import *

urlpatterns = [
    # Get bid for pk
    path('<int:ad_pk>/<int:bid_pk>/', BidRetrieveAPIView.as_view()),  # Оптимизированно

    # Create bid
    path('create', BidCreateView.as_view()),  # Оптимизированно

    # Delete bid for pk
    path('remove/<int:pk>/', BidRejected.as_view()),  # Оптимизированно

    # Receiving my bids for pk
    path('my_bids/<int:pk>/', MyBidsRetrieveAPIView.as_view())  # Оптимизированно
]
