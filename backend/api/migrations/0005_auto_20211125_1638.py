# Generated by Django 3.1.7 on 2021-11-25 16:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20211121_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldofstudy',
            name='students',
        ),
        migrations.AlterField(
            model_name='semester',
            name='semester',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
    ]
