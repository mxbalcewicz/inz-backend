# Generated by Django 3.1.7 on 2021-10-10 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_ectscard_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ectscard',
            name='name',
        ),
    ]
