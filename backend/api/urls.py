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
                    SemesterGetPostView,
                    ECTSCardGetPostView,
                    ECTSCardRetrieveUpdateDeleteView,
FieldGroupGetPostView,
FieldGroupRetrieveUpdateDeleteView,
TimeTableUnitRetrieveUpdateDeleteView,
TimeTableUnitGetPostView,
TimeTableGetPostView,
TimeTableRetrieveUpdateDeleteView

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
    path('ectscard/', ECTSCardGetPostView.as_view(), name='ectscard_post_get'),
    path('ectscard/<int:pk>', ECTSCardRetrieveUpdateDeleteView.as_view(), name='ectscard_update_delete'),
    path('fieldgroup/', FieldGroupGetPostView.as_view(), name='field_group_post_get'),
    path('fieldgroup/<int:pk>', FieldGroupRetrieveUpdateDeleteView.as_view(), name='field_group_update_delete'),
    path('timetable/', TimeTableGetPostView.as_view(), name='timetable_post_get'),
    path('timetable/<int:pk>', TimeTableRetrieveUpdateDeleteView.as_view(), name='timetable_update_delete'),
    path('timetableunit/', TimeTableUnitGetPostView.as_view(), name='timetableunit_post_get'),
    path('timetableunit/<int:pk>', TimeTableUnitRetrieveUpdateDeleteView.as_view(), name='timetableunit_update_delete'),


]
