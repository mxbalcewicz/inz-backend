from django.urls import path, include
from django.views.generic import base
from rest_framework.routers import DefaultRouter
from .views import (
    CourseDocumentView,
    ECTSCardDocumentView,
    RoomDocumentView,
    SearchAllDocumentsView,
    SemesterDocumentView,
    StudentDocumentView,
    FieldGroupDocumentView,
    FieldOfStudyDocumentView,
    StaffAccountDocumentView,
    DeaneryAccountDocumentView,
    CourseInstructorInfoDocumentView
)
router = DefaultRouter(trailing_slash=False)

router.register(r'students', StudentDocumentView,
                basename='student_document_view')
router.register(r'rooms', RoomDocumentView, basename='room_document_view')
router.register(r'fieldgroup', FieldGroupDocumentView,
                basename='fieldgroup_document_view')
router.register(r'fieldofstudy', FieldOfStudyDocumentView,
                basename='fieldofstudy_document_view')
router.register(r'staffaccount', StaffAccountDocumentView,
                basename='staffaccount_document_view')
router.register(r'deaneryaccount', DeaneryAccountDocumentView,
                basename='deaneryaccount_document_view')
router.register(r'courseinstructorinfo', CourseInstructorInfoDocumentView,
                basename='courseinstructorinfo_document_view')
router.register(r'semester', SemesterDocumentView,
                basename='semester_document_view')
router.register(r'course', CourseDocumentView, basename='course_document_view')
router.register(r'ectscard', ECTSCardDocumentView,
                basename='ectscard_document_view')

urlpatterns = [
    path('', include(router.urls)),
    path('all/<query>', SearchAllDocumentsView.as_view(), name='all_documents_view')
]
