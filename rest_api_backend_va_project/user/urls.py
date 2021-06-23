from django.urls import path

from .views import *

urlpatterns = [
    # Get all users
    path('all', UserListView.as_view()),  # Оптимизированно

    # Get user for id
    path('user/<int:pk>/', UserRetrieveAPIView.as_view()),  # Оптимизированно

    # Update my data
    path('update/<int:pk>/', UserUpdateData.as_view()),

    # Information about me
    path('me/', GetDataAboutMe.as_view()),  # Оптимизированно

    # Auth
    # Registration
    path('auth/signup', RegisterView.as_view()),  # Оптимизированно частично

    # Login
    path('auth/verify-code', VerifyCode.as_view(), name='verify-code'),  # Оптимизированно

    # Forget password
    path('auth/forget-password', ForgetPassword.as_view(), name='forget-password'),  # Оптимизированно
    path('auth/verify-forget-password', VerifyForgetPassword.as_view(), name='verify-forget-password'),  # Оптимизированно
    path('auth/addPassword-forget-password', AddPasswordForgetPassword.as_view(), name='addPassword-forget-password'),  # Оптимизированно

    # Change password
    path('auth/change-password', ChangePasswordView.as_view(), name='change-password'),  # Оптимизированно

    # Subscription
    path('subscribers/', SubscriptionAPIView.as_view()),
    path('my_subscriber/', MySubscriber.as_view())
]
