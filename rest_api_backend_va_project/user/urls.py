from django.urls import path

from .views import *

urlpatterns = [
    # Get all users
    path('all', UserListView.as_view()),

    # Create user
    path('create', UserCreateView.as_view()),

    # Get user for id
    path('user/<int:pk>/', UserRetrieveAPIView.as_view()),

    # Update my data
    path('update/<int:pk>/', UserUpdateData.as_view()),

    # Information about me
    path('me/', GetDataAboutMe.as_view()),

    # Auth
    # Registration
    path('auth/signup', RegisterView.as_view()),
    # Login
    path('auth/verify-code', verify_code, name='verify-code'),

    # Forget password
    path('auth/forget-password', forget_password, name='forget-password'),
    path('auth/verify-forget-password', verify_forget_password, name='verify-forget-password'),
    path('auth/addPassword-forget-password', add_password_forget_password, name='addPassword-forget-password'),

    # Change password
    path('auth/change-password', ChangePasswordView.as_view(), name='change-password'),
]
