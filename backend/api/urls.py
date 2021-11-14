from django.urls import path

from .views import (StudentGetPostView,
                    StudentRetrieveUpdateDeleteView,
                    StaffUserViewSet,
                    FieldOfStudyViewSet,
                    CourseViewSet,
                    RoomGetPostView,
                    RoomRetrieveUpdateDeleteView,
                    CourseInstructorInfoGetPostView,
                    CourseInstructorInfoRetrieveUpdateDeleteView,
                    )

urlpatterns = [
    path('students/', StudentGetPostView.as_view(), name='students'),
    path('students/<int:pk>', StudentRetrieveUpdateDeleteView.as_view(), name='students_update_delete'),
    path('courseinstructorinfo/', CourseInstructorInfoGetPostView.as_view(), name='courseinstructorinfo'),
    path('courseinstructorinfo/<int:pk>', CourseInstructorInfoRetrieveUpdateDeleteView.as_view(),
         name='courseinstructorinfo_update_delete'),
    path('staff/', StaffUserViewSet, name='staff'),
    path('fieldsofstudy/', FieldOfStudyViewSet, name='fieldofstudy'),
    path('courses/', CourseViewSet, name='courses'),
    path('rooms/', RoomGetPostView.as_view(), name='rooms_post_get'),
    path('rooms/<int:pk>', RoomRetrieveUpdateDeleteView.as_view(), name='rooms_update_delete'),
    # path('ectscards/', ECTSCardView.as_view(), name='ectscards'),
    # path('coursesinstructorinfo/', CourseInstructorInfoViewSet, name='courseinstructorinfo'),
    # path('semesters/', SemesterViewSet, name='rooms'),
]
