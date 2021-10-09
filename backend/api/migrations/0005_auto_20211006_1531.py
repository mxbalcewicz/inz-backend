# Generated by Django 3.1.7 on 2021-10-06 15:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20211004_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_type',
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('LECTURE', 'LECTURE'), ('LABORATORY', 'LABORATORY'), ('PROJECT', 'PROJECT'), ('SPORT_HALL', 'SPORT_HALL')], max_length=20), default=['LECTURE'], size=None),
        ),
        migrations.DeleteModel(
            name='RoomType',
        ),
    ]