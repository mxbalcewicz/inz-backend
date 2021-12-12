from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentDocumentView

router = DefaultRouter()

students = router.register(r'students', StudentDocumentView, basename='studentdocument')
urlpatterns = [
    path('', include(router.urls)),
]