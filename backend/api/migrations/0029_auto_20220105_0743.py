# Generated by Django 3.1.7 on 2022-01-05 07:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20220103_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='semester_end_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 5, 7, 43, 8, 535828)),
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester_start_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 5, 7, 43, 8, 535813)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='end_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 5, 7, 43, 8, 538931)),
        ),
        migrations.AlterField(
            model_name='timetableunit',
            name='start_hour',
            field=models.TimeField(default=datetime.datetime(2022, 1, 5, 7, 43, 8, 538917)),
        ),
    ]
