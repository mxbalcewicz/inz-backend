from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import DeanAccountGetPostView, DeanAccountRetrieveUpdateDeleteView, StaffAccountGetPostView, StaffAccountRetrieveUpdateDeleteView

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('dean', DeanAccountGetPostView.as_view(), name='dean_get_post'),
    path('dean/<int:pk>', DeanAccountRetrieveUpdateDeleteView.as_view(), name='dean_retrieve_update_delete'),
    path('staff', StaffAccountGetPostView.as_view(), name='staff_get_post'),
    path('staff/<int:pk>', StaffAccountRetrieveUpdateDeleteView.as_view(), name='staff_retrieve_update_delete'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
