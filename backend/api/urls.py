from django.urls import path

from .views import (StudentViewSet,
                    StaffUserViewSet,
                    FieldOfStudyViewSet,
                    CourseViewSet,
                    RoomViewSet, RoomGetPostView, RoomRetrieveUpdateDeleteView
                    )

urlpatterns = [
    path('students/', StudentViewSet, name='students'),
    path('staff/', StaffUserViewSet, name='staff'),
    path('fieldsofstudy/', FieldOfStudyViewSet, name='fieldofstudy'),
    path('courses/', CourseViewSet, name='courses'),
    path('rooms/', RoomGetPostView.as_view(), name='rooms_post_get'),
    path('rooms/<int:pk>', RoomRetrieveUpdateDeleteView.as_view(), name='rooms_update_delete'),
    # path('ectscards/', ECTSCardView.as_view(), name='ectscards'),
    # path('coursesinstructorinfo/', CourseInstructorInfoViewSet, name='courseinstructorinfo'),
    # path('semesters/', SemesterViewSet, name='rooms'),
]
