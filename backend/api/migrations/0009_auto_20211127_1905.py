# Generated by Django 3.1.7 on 2021-11-27 19:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20211127_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='semester_end_date',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='semester_start_date',
        ),
        migrations.AddField(
            model_name='semester',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 27, 19, 5, 37, 315880)),
        ),
        migrations.AddField(
            model_name='semester',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 27, 19, 5, 37, 315863)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2021, 11, 27, 19, 5, 37, 319629)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2021, 11, 27, 19, 5, 37, 319613)),
        ),
    ]
