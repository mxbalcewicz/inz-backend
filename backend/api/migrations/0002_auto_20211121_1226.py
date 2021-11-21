# Generated by Django 3.1.7 on 2021-11-21 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTableUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'), ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY')], default='MONDAY', max_length=30)),
                ('hour', models.CharField(choices=[('8:00-9:30', '8:00-9:30'), ('9:45-11:45', '9:45-11:45'), ('11:45-13:15', '11:45-13:15'), ('13:30-15:00', '13:30-15:00'), ('15:10-16:40', '15:10-16:40'), ('16:50-18:20', '16:50-18:20'), ('18:30-20:00', '18:30-20:00')], default='8:00-9:30', max_length=30)),
                ('week', models.CharField(choices=[('EVEN', 'EVEN'), ('ODD', 'ODD'), ('ALL', 'ALL')], default='ALL', max_length=30)),
                ('course_instructor_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.courseinstructorinfo')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.semester')),
                ('time_table_units', models.ManyToManyField(blank=True, to='api.TimeTableUnit')),
            ],
        ),
        migrations.AddField(
            model_name='fieldofstudy',
            name='field_groups',
            field=models.ManyToManyField(blank=True, to='api.FieldGroup'),
        ),
    ]
