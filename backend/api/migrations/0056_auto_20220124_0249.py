# Generated by Django 3.1.7 on 2022-01-24 02:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0055_auto_20220124_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 24, 2, 49, 10, 941294)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 24, 2, 49, 10, 941278)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 24, 2, 49, 10, 944632)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 24, 2, 49, 10, 944616)),
        ),
    ]