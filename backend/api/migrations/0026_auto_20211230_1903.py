# Generated by Django 3.1.7 on 2021-12-30 19:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20211230_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 30, 19, 3, 56, 587898)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 30, 19, 3, 56, 587882)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2021, 12, 30, 19, 3, 56, 591730)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2021, 12, 30, 19, 3, 56, 591714)),
        ),
    ]