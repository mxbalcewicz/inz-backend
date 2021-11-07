from rest_framework.routers import DefaultRouter
from .views import (StudentViewSet,
                    StaffUserViewSet,
                    FieldOfStudyViewSet,
                    CourseViewSet,
                    RoomViewSet,
                    ECTSCardViewSet,
                    CourseInstructorInfoViewSet,
                    SemesterViewSet
                    )

router = DefaultRouter(trailing_slash=False)

router.register(r'students/', StudentViewSet, basename='students')
router.register(r'staff/', StaffUserViewSet, basename='staff')
router.register(r'fieldsofstudy/', FieldOfStudyViewSet, basename='fieldofstudy')
router.register(r'courses/', CourseViewSet, basename='courses')
router.register(r'rooms/', RoomViewSet, basename='rooms')
router.register(r'ectscards/', ECTSCardViewSet, basename='ectscards')
router.register(r'coursesinstructorinfo/', CourseInstructorInfoViewSet, basename='courseinstructorinfo')
router.register(r'semesters/', SemesterViewSet, basename='rooms')

urlpatterns = router.urls
