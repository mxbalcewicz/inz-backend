from django.db import models


# Create your models here.

class Student(models.Model):
    email = models.EmailField(max_length=50, unique=True, blank=False)
    index = models.CharField(max_length=8, blank=False)
    name = models.CharField(max_length=20, blank=False)
    surename = models.CharField(max_length=30, blank=False)


class StudyType(models.Model):  # typ studiów
    STATIONARY = 1
    NOSTATIONARY = 2
    STUDY_TYPES = (
        (STATIONARY, 'STATIONARY'),
        (NOSTATIONARY, 'NOSTATIONARY')
    )

    id = models.PositiveSmallIntegerField(choices=STUDY_TYPES, primary_key=True)


class FieldOfStudy(models.Model):
    studyType = models.OneToOneField(StudyType, on_delete=models.CASCADE, blank=False, primary_key=False)
    start_date = models.DateTimeField(auto_now_add=False)
    students = models.ManyToManyField(Student, blank=True)


class RoomType(models.Model):
    LECTURE = 1
    LABORATORY = 2
    PROJECT = 3
    SPORT_HALL = 4
    ROOM_TYPES = (
        (LECTURE, 'LECTURE'),
        (LABORATORY, 'LABORATORY'),
        (PROJECT, 'PROJECT'),
        (SPORT_HALL, 'SPORT_HALL')
    )

    id = models.PositiveSmallIntegerField(choices=ROOM_TYPES, primary_key=True)


class Room(models.Model):
    name = models.CharField(max_length=20, blank=False, unique=True)
    capacity = models.CharField(max_length=4, blank=False)
    roomType = models.ManyToManyField(RoomType, blank=False, primary_key=False)


class Lecturer(models.Model):
    user = models.OneToOneField('accounts.StaffAccount', on_delete=models.CASCADE, blank=False, primary_key=True)
    name = models.CharField(max_length=20, blank=False)
    surename = models.CharField(max_length=30, blank=False)
    institut = models.CharField(max_length=100, blank=False)
    jobTitle = models.CharField(max_length=50, blank=False)  # better name needed (stanowisko)
    academic_title = models.CharField(max_length=50, blank=False)
