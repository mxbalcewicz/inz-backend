from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterDeanAccountView, RegisterStaffAccountView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-dean/', RegisterDeanAccountView.as_view(), name='register_dean'),
    path('register-staff/', RegisterStaffAccountView.as_view(), name='register_staff'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
