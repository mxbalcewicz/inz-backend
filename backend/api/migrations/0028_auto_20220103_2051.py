# Generated by Django 3.1.7 on 2022-01-03 20:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_merge_20211230_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ectscard',
            name='courses',
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 3, 20, 51, 31, 811113)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 3, 20, 51, 31, 811095)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 3, 20, 51, 31, 814242)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 3, 20, 51, 31, 814227)),
        ),
    ]
