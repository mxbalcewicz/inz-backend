from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import StaffAccount
from datetime import datetime


class Course(models.Model):
    LECTURE = 'Lecture'
    LABORATORY = 'Laboratory'
    PROJECT = 'Project'
    PRACTICALS = 'Practicals'

    CLASS_TYPE_CHOICES = [
        (LECTURE, 'Lecture'),
        (LABORATORY, 'Laboratory'),
        (PROJECT, 'Project'),
        (PRACTICALS, 'Practicals'),
    ]
    name = models.CharField(blank=False, max_length=50)
    hours = models.IntegerField(blank=False, null=False, validators=[
        MinValueValidator(1),
        MaxValueValidator(60),
    ])
    class_type = models.CharField(choices=CLASS_TYPE_CHOICES, default=LECTURE, max_length=45)
    points_value = models.IntegerField(blank=False, null=False, validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    instructors = models.ManyToManyField(StaffAccount)


class Student(models.Model):
    email = models.EmailField(max_length=50, unique=True, blank=False)
    index = models.CharField(max_length=8, blank=False)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=30, blank=False)


# class StudyType(models.Model):  # typ studiów
#     STATIONARY = 1
#     NOSTATIONARY = 2
#     STUDY_TYPES = (
#         (STATIONARY, 'STATIONARY'),
#         (NOSTATIONARY, 'NOSTATIONARY')
#     )
#
#     id = models.PositiveSmallIntegerField(choices=STUDY_TYPES, primary_key=True)


class FieldOfStudy(models.Model):
    FULL_TIME = 'Full time'
    PART_TIME = 'Part time'
    STUDY_TYPES = (
        (FULL_TIME, 'Full time'),
        (PART_TIME, 'Part time'),
    )

    study_type = models.CharField(default=FULL_TIME, choices=STUDY_TYPES, blank=False, null=False, max_length=10)
    start_date = models.DateTimeField(auto_now_add=False, default=datetime.now)
    end_date = models.DateTimeField(auto_now_add=False, default=datetime.now)
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
    room_type = models.ManyToManyField(RoomType, blank=False, primary_key=False)


# class Lecturer(models.Model):
#     user = models.OneToOneField('accounts.StaffAccount', on_delete=models.CASCADE, blank=False, primary_key=True)
#     name = models.CharField(max_length=20, blank=False)
#     surename = models.CharField(max_length=30, blank=False)
#     institut = models.CharField(max_length=100, blank=False)
#     jobTitle = models.CharField(max_length=50, blank=False)  # better name needed (stanowisko)
#     academic_title = models.CharField(max_length=50, blank=False)


class ECTSCard(models.Model):
    courses = models.ManyToManyField(Course)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    semester = models.IntegerField()
    year = models.IntegerField()