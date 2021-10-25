from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import StaffAccount
from datetime import date


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
    index = models.IntegerField(unique=True, blank=False, default=1)
    email = models.EmailField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f'Mail:{self.email},  Name:{self.name}, Surname:{self.surname}, Index:{self.index}'


class FieldOfStudy(models.Model):
    FULL_TIME = 'FULL_TIME'
    PART_TIME = 'PART_TIME'
    STUDY_TYPES = (
        (FULL_TIME, 'FULL_TIME'),
        (PART_TIME, 'PART_TIME'),
    )

    name = models.CharField(max_length=60, blank=True, default='Untitled')
    study_type = models.CharField(default=FULL_TIME, choices=STUDY_TYPES, blank=True, null=False, max_length=10)
    start_date = models.DateField(auto_now_add=False, default=date.today)
    end_date = models.DateField(auto_now_add=False, default=date.today)
    students = models.ManyToManyField(Student, blank=False)

    def __str__(self):
        return f'Name:{self.name} Type:{self.study_type} Start:{self.start_date} End:{self.end_date}'


class Room(models.Model):
    LECTURE = 'LECTURE'
    LABORATORY = 'LABORATORY'
    PROJECT = 'PROJECT'
    SPORT_HALL = 'SPORT_HALL'
    ROOM_TYPES = (
        (LECTURE, 'LECTURE'),
        (LABORATORY, 'LABORATORY'),
        (PROJECT, 'PROJECT'),
        (SPORT_HALL, 'SPORT_HALL')
    )

    name = models.CharField(max_length=20, blank=False, unique=True)
    capacity = models.CharField(max_length=4, blank=False)
    room_type = ArrayField(models.CharField(choices=ROOM_TYPES, max_length=20, blank=True), default=['LECTURE'])


class ECTSCard(models.Model):
    courses = models.ManyToManyField(Course)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    semester = models.IntegerField()
    year = models.IntegerField()