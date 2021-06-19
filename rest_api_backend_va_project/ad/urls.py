from django.urls import path
from .views import *

urlpatterns = [
    # Получение всех объявлений
    path('all', AdListView.as_view()),  # Оптимизированно

    # Создание объявления
    path('create', AdCreateView.as_view()),  # Оптимизированно

    # Изменение объявления
    path('update/<int:pk>/', AdUpdateView.as_view()),  # Оптимизированно

    # Получение объявления по pk
    path('ad/<int:pk>/', AdRetrieveAPIView.as_view()),  # Оптимизированно

    # Удаление объявления по pk
    path('remove/<int:pk>', AdDestroyAPIView.as_view()),  # Оптимизированно

    # Получение всех моих объявление
    path('my_ads/', MyAdsListAPIView.as_view())  # Оптимизированно
]
