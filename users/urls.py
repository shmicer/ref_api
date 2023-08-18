from django.urls import path

from .views import SMSCodeVerificationView, UserAPIView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('verify-sms/', SMSCodeVerificationView.as_view(), name='verify-sms'),
    path("<str:phone_number>", UserAPIView.as_view(), name="user-info"),
]
