from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StaffUserViewSet, FieldOfStudyViewSet, CourseViewSet, RoomViewSet

router = DefaultRouter()

router.register(r'students', StudentViewSet, basename='students')
router.register(r'staff', StaffUserViewSet, basename='staff')
router.register(r'fieldsofstudy', FieldOfStudyViewSet, basename='fieldofstudy')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'rooms', RoomViewSet, basename='rooms')


urlpatterns = router.urls
