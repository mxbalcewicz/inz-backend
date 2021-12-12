from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomDocumentView, StudentDocumentView

router = DefaultRouter()

router.register(r'students', StudentDocumentView, basename='studentdocumentview')
router.register(r'rooms', RoomDocumentView, basename='roomdocumentview')

urlpatterns = [
    path('', include(router.urls)),
]