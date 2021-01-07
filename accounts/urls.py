from django.urls import path

from .views import *
from django.conf.urls.static import static
from banking_system import settings
from accounts.views import UserLoginView
from accounts.views import LogoutView
from accounts.views import UserRegistrationView
from django.contrib.auth import views



app_name = 'accounts'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    # path('login/', LoginView.as_view(), name='user_login'),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView,
        name="user_registration"
    ),
    path(
        "checkfingerprint/", checkFingerprintupload,
        name="checkfingerprint"
    ),
    # path(
    #     "checker/", checkFingerprint,
    #     name="checker"
    # ),
    path(
        "otp/", OTPCheck,
        name="OTP"
    ),
    path('password_change/', passwordChange, name='password_change'),
]

