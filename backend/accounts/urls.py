from ast import Pass
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    DeanAccountGetPostView,
    StaffAccountGetPostView,
    StaffAccountRetrieveUpdateDeleteView,
    DeanAccountRetrieveUpdateDeleteView,
    VerifyEmail,
    ResendVerifyEmail,
    PasswordTokenCheckAPI,
    RequestPasswordResetEmail,
    SetNewPasswordView,
    Login, Logout, Refresh
)

urlpatterns = [
    path('dean', DeanAccountGetPostView.as_view(), name='dean_get_post'),
    path('dean/<int:pk>', DeanAccountRetrieveUpdateDeleteView.as_view(), name='dean_retrieve_update_delete'),
    path('staff', StaffAccountGetPostView.as_view(), name='staff_get_post'),
    path('staff/<int:pk>', StaffAccountRetrieveUpdateDeleteView.as_view(), name='staff_retrieve_update_delete'),
    path('activate-account', VerifyEmail.as_view(), name="activate-account"),
    path('resend-activate-account', ResendVerifyEmail.as_view(), name="resend-email-verify"),
    path('reset-password/<uidb64>/<token>', PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path('request-reset-password', RequestPasswordResetEmail.as_view(), name="request-password-reset-email"),
    path('reset-password', SetNewPasswordView.as_view(), name='password-reset-complete'),
    path('login', Login.as_view(), name='login-view'),
    path('logout', Logout.as_view(), name='logout-view'),
    path('refresh', Refresh.as_view(), name='refresh-view')
]
