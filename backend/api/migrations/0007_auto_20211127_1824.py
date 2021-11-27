# Generated by Django 3.1.7 on 2021-11-27 18:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20211127_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 27, 18, 24, 27, 809822)),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 27, 18, 24, 27, 809809)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2021, 11, 27, 18, 24, 27, 808893)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2021, 11, 27, 18, 24, 27, 808876)),
        ),
    ]
