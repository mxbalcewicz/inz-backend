# Generated by Django 3.1.7 on 2021-11-27 18:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20211125_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetableunit',
            name='hour',
        ),
        migrations.AddField(
            model_name='course',
            name='balance_of_work_of_an_avg_student',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='content_of_the_subject',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='didactic_methods',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='literature',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='methods_of_verification_of_learning_outcomes_and_criteria',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='purposes',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='subject_learning_outcomes',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='timetable',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 27, 18, 15, 48, 581637)),
        ),
        migrations.AddField(
            model_name='timetable',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 27, 18, 15, 48, 581624)),
        ),
        migrations.AddField(
            model_name='timetableunit',
            name='end_hour',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 27, 18, 15, 48, 580700)),
        ),
        migrations.AddField(
            model_name='timetableunit',
            name='start_hour',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 27, 18, 15, 48, 580683)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='day',
            field=models.CharField(choices=[('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'), ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY'), ('SATURDAY', 'SATURDAY'), ('SUNDAY', 'SUNDAY')], default='MONDAY', max_length=30),
        ),
    ]