from django.urls import path

from .views import (StudentGetPostView,
                    StudentRetrieveUpdateDeleteView,
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
                    TimeTableRetrieveUpdateDeleteView,
                    StudentsCSVExportView,
                    RoomsCSVExportView,
                    CourseCSVExportView,
                    SemesterCSVExportView,
                    FieldGroupCSVExportView,
                    FieldOfStudyCSVExportView,
                    ECTSCardCSVExportView,
                    TimeTableCSVExportView,
                    TimeTableUnitCSVExportView,
                    RoomCSVImportView,
                    CourseInstructorInfosCSVExportView,
                    CourseCSVImportView,
                    CourseInstructorInfosCSVImportView,
                    StudentsCSVImportView,
                    SemesterCSVImportView,
                    FieldGroupCSVImportView,
                    FieldOfStudyCSVImportView,
                    ECTSCardCSVImportView,
                    )

urlpatterns = [
    path('students', StudentGetPostView.as_view(), name='student_get_post'),
    path('students/export/csv', StudentsCSVExportView.as_view(), name='export-csv-students'),
    path('students/import/csv', StudentsCSVImportView.as_view(), name='import-csv-students'),
    path('students/<int:pk>', StudentRetrieveUpdateDeleteView.as_view(), name='student_update_delete'),
    path('courseinstructorinfo', CourseInstructorInfoGetPostView.as_view(), name='courseinstructorinfo_get_post'),
    path('courseinstructorinfo/<int:pk>', CourseInstructorInfoRetrieveUpdateDeleteView.as_view(),
         name='courseinstructorinfo_update_delete'),
    path('courseinstructorinfo/export/csv', CourseInstructorInfosCSVExportView.as_view(),
         name='export-csv-courseinstructorinfo'),
    path('courseinstructorinfo/import/csv', CourseInstructorInfosCSVImportView.as_view(),
         name='import-csv-courseinstructorinfo'),
    path('course', CourseGetPostView.as_view(), name='course_get_post'),
    path('course/<int:pk>', CourseRetrieveUpdateDeleteView.as_view(),
         name='course_update_delete'),
    path('course/export/csv', CourseCSVExportView.as_view(), name='export-csv-courses'),
    path('course/import/csv', CourseCSVImportView.as_view(), name='import-csv-courses'),
    path('rooms', RoomGetPostView.as_view(), name='room_get_post'),
    path('rooms/<int:pk>', RoomRetrieveUpdateDeleteView.as_view(), name='room_update_delete'),
    path('rooms/export/csv', RoomsCSVExportView.as_view(), name='export-csv-rooms'),
    path('fieldofstudy', FieldOfStudyGetPostView.as_view(), name='fieldofstudy_get_post'),
    path('fieldofstudy/<int:pk>', FieldOfStudyRetrieveUpdateDeleteView.as_view(), name='fieldofstudy_update_delete'),
    path('fieldofstudy/export/csv', FieldOfStudyCSVExportView.as_view(), name='export-csv-fieldofstudy'),
    path('fieldofstudy/import/csv', FieldOfStudyCSVImportView.as_view(), name='import-csv-fieldofstudy'),
    path('semester/', SemesterGetPostView.as_view(), name='semester_get_post'),
    path('semester/<int:pk>', SemesterRetrieveUpdateDeleteView.as_view(), name='semester_update_delete'),
    path('semester/export/csv', SemesterCSVExportView.as_view(), name='export-csv-semesters'),
    path('semester/import/csv', SemesterCSVImportView.as_view(), name='import-csv-semesters'),
    path('ectscard', ECTSCardGetPostView.as_view(), name='ectscard_get_post'),
    path('ectscard/<int:pk>', ECTSCardRetrieveUpdateDeleteView.as_view(), name='ectscard_update_delete'),
    path('ectscard/export/csv', ECTSCardCSVExportView.as_view(), name='export-csv-ectscard'),
    path('ectscard/import/csv', ECTSCardCSVImportView.as_view(), name='import-csv-ectscard'),
    path('fieldgroup', FieldGroupGetPostView.as_view(), name='field_group_get_post'),
    path('fieldgroup/<int:pk>', FieldGroupRetrieveUpdateDeleteView.as_view(), name='field_group_update_delete'),
    path('fieldgroup/export/csv', FieldGroupCSVExportView.as_view(), name='export-csv-fieldgroup'),
    path('fieldgroup/import/csv', FieldGroupCSVImportView.as_view(), name='import-csv-fieldgroup'),
    path('timetable', TimeTableGetPostView.as_view(), name='timetable_get_post'),
    path('timetable/<int:pk>', TimeTableRetrieveUpdateDeleteView.as_view(), name='timetable_update_delete'),
    path('timetable/export/csv', TimeTableCSVExportView.as_view(), name='export-csv-timetable'),
    path('timetableunit', TimeTableUnitGetPostView.as_view(), name='timetableunit_get_post'),
    path('timetableunit/<int:pk>', TimeTableUnitRetrieveUpdateDeleteView.as_view(), name='timetableunit_update_delete'),
    path('timetableunit/export/csv', TimeTableUnitCSVExportView.as_view(), name='export-csv-timetableunit'),
    path('rooms/import/csv', RoomCSVImportView.as_view(), name='import-csv-room')
]
