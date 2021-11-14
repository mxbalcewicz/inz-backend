from django.urls import path

from .views import (StudentGetPostView,
                    StudentRetrieveUpdateDeleteView,
                    StaffUserViewSet,
                    RoomGetPostView,
                    RoomRetrieveUpdateDeleteView,
                    CourseInstructorInfoGetPostView,
                    CourseInstructorInfoRetrieveUpdateDeleteView,
                    CourseGetPostView,
                    CourseRetrieveUpdateDeleteView,
                    FieldOfStudyGetPostView,
                    FieldOfStudyRetrieveUpdateDeleteView,
                    SemesterRetrieveUpdateDeleteView,
                    SemesterGetPostView
                    )

urlpatterns = [
    path('students/', StudentGetPostView.as_view(), name='students'),
    path('students/<int:pk>', StudentRetrieveUpdateDeleteView.as_view(), name='students_update_delete'),
    path('courseinstructorinfo/', CourseInstructorInfoGetPostView.as_view(), name='courseinstructorinfo'),
    path('courseinstructorinfo/<int:pk>', CourseInstructorInfoRetrieveUpdateDeleteView.as_view(),
         name='courseinstructorinfo_update_delete'),
    path('course/', CourseGetPostView.as_view(), name='course'),
    path('course/<int:pk>', CourseRetrieveUpdateDeleteView.as_view(),
         name='course_update_delete'),
    path('staff/', StaffUserViewSet, name='staff'),
    path('rooms/', RoomGetPostView.as_view(), name='rooms_post_get'),
    path('rooms/<int:pk>', RoomRetrieveUpdateDeleteView.as_view(), name='rooms_update_delete'),
    path('fieldofstudy/', FieldOfStudyGetPostView.as_view(), name='fieldofstudy_post_get'),
    path('fieldofstudy/<int:pk>', FieldOfStudyRetrieveUpdateDeleteView.as_view(), name='fieldofstudy_update_delete'),
    path('semester/', SemesterGetPostView.as_view(), name='semester_post_get'),
    path('semester/<int:pk>', SemesterRetrieveUpdateDeleteView.as_view(), name='semester_update_delete'),

]
