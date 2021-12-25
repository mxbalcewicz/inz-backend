# Generated by Django 3.1.7 on 2021-12-23 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20211219_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 23, 19, 2, 47, 241032)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 23, 19, 2, 47, 241013)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2021, 12, 23, 19, 2, 47, 245999)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2021, 12, 23, 19, 2, 47, 245979)),
        ),
    ]