from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import StaffAccount
from datetime import date


class CourseInstructorInfo(models.Model):
    LECTURE = 'LECTURE'
    LABORATORY = 'LABORATORY'
    PROJECT = 'PROJECT'
    COURSE_TYPES = (
        (LECTURE, 'LECTURE'),
        (LABORATORY, 'LABORATORY'),
        (PROJECT, 'PROJECT')
    )
    hours = models.IntegerField(blank=False, null=False, default=15, validators=[
        MinValueValidator(1),
        MaxValueValidator(60),
    ])
    instructor = models.ForeignKey(StaffAccount, on_delete=models.CASCADE)
    course_type = models.CharField(default=LECTURE, choices=COURSE_TYPES, blank=False, max_length=15)

    def __str__(self):
        instructor = StaffAccount.objects.get(pk=self.instructor)
        return f'Course type:{self.course_type}, Hours:{self.hours}, Instructor:{instructor.account.email}'


class Student(models.Model):
    index = models.IntegerField(unique=True, blank=False, default=1)
    email = models.EmailField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f'Mail:{self.email},  Name:{self.name}, Surname:{self.surname}, Index:{self.index}'


class Course(models.Model):
    name = models.CharField(blank=False, max_length=50)
    course_instructor_info = models.ManyToManyField(CourseInstructorInfo, blank=False)
    points_value = models.IntegerField(blank=False, null=False, validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])

    def __str__(self):
        course_instructor_infos = [i.id for i in self.course_instructor_info.all()]
        return f'Id:{self.pk}, Name:{self.name}, Instructor info ids:{course_instructor_infos}, Points value:{self.points_value}'


class Semester(models.Model):
    semester = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(12),
    ])
    year = models.IntegerField()
    students = models.ManyToManyField(Student, blank=True)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=False)

    def __str__(self):
        return f'Semester:{self.semester}, Year:{self.year}, FieldOfStudy:{self.field_of_study.name}'


class FieldGroup(models.Model):
    """
        Field Group eg. TI-1-1, TI-1-2, BSI-2-1
    """
    name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f'Name:{self.name}'


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
    field_groups = models.ManyToManyField(FieldGroup, blank=True)

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
    # Sprawdzic opcje zmiany ArrayField na inne przy multiple choice
    room_type = ArrayField(models.CharField(choices=ROOM_TYPES, max_length=20, blank=True), default=['LECTURE'])


class ECTSCard(models.Model):
    courses = models.ManyToManyField(Course, blank=False)
    field_of_study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)


class TimeTableUnit(models.Model):
    MONDAY = 'MONDAY'
    TUESDAY = 'TUESDAY'
    WEDNESDAY = 'WEDNESDAY'
    THURSDAY = 'THURSDAY'
    FRIDAY = 'FRIDAY'
    SATURDAY = 'SATURDAY'
    SUNDAY = 'SUNDAY'
    DAYS = (
        (MONDAY, 'MONDAY'),
        (TUESDAY, 'TUESDAY'),
        (WEDNESDAY, 'WEDNESDAY'),
        (THURSDAY, 'THURSDAY'),
        (FRIDAY, 'FRIDAY'),
        (SATURDAY, 'SATURDAY'),
        (SUNDAY, 'SUNDAY')
    )

    FIRST = '8:00-9:30'
    SECOND = '9:45-11:30'
    THIRD = '11:45-13:15'
    FOURTH = '13:30-15:00'
    FIFTH = '15:10-16:40'
    SIXTH = '16:50-18:20'
    SEVENTH = '18:30-20:00'
    HOURS = (
        (FIRST, '8:00-9:30'),
        (SECOND, '9:45-11:45'),
        (THIRD, '11:45-13:15'),
        (FOURTH, '13:30-15:00'),
        (FIFTH, '15:10-16:40'),
        (SIXTH, '16:50-18:20'),
        (SEVENTH, '18:30-20:00')
    )

    EVEN = 'EVEN'
    ODD = 'ODD'
    ALL = 'ALL'
    WEEKS = (
        (EVEN, 'EVEN'),
        (ODD, 'ODD'),
        (ALL, 'ALL')
    )

    day = models.CharField(default=MONDAY, choices=DAYS, blank=False, max_length=30)
    hour = models.CharField(default=FIRST, choices=HOURS, blank=False, max_length=30)
    week = models.CharField(default=ALL, choices=WEEKS, blank=False, max_length=30)
    course_instructor_info = models.ForeignKey('CourseInstructorInfo', blank=False, on_delete=models.CASCADE)
    field_groups = models.ManyToManyField(FieldGroup, blank=False)


class TimeTable(models.Model):
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    time_table_units = models.ManyToManyField(TimeTableUnit, blank=True)
