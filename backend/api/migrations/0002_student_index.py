# Generated by Django 3.1.7 on 2021-10-25 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='index',
            field=models.IntegerField(default=1, unique=True),
        ),
    ]
