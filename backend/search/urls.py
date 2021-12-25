from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomDocumentView,
    StudentDocumentView,
    FieldGroupDocumentView,
    FieldOfStudyDocumentView,
    StaffAccountDocumentView
)
router = DefaultRouter()

router.register(r'students', StudentDocumentView, basename='studentdocumentview')
router.register(r'rooms', RoomDocumentView, basename='roomdocumentview')
router.register(r'fieldgroup', FieldGroupDocumentView, basename='fieldgroup_document_view')
router.register(r'fieldofstudy', FieldOfStudyDocumentView, basename='fieldofstudy_document_view')
router.register(r'staffaccount', StaffAccountDocumentView, basename='staffaccount_document_view')

urlpatterns = [
    path('', include(router.urls)),
]