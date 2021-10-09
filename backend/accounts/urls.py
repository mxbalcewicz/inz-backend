from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import DeanRegisterView, StaffRegisterView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-dean/', DeanRegisterView.as_view(), name='register_dean'),
    path('register-staff/', StaffRegisterView.as_view(), name='register_staff'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
