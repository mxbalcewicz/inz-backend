# Generated by Django 3.1.7 on 2022-01-17 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20220117_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 17, 13, 14, 9, 568991)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 17, 13, 14, 9, 568971)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 17, 13, 14, 9, 573083)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 17, 13, 14, 9, 573065)),
        ),
    ]
