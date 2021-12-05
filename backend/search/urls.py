from django.urls import path

from search.views import SearchStudents

urlpatterns = [
    path('student/<str:query>/', SearchStudents.as_view()),

]