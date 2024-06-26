# Generated by Django 5.0 on 2023-12-27 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=1000)),
                ('link', models.CharField(max_length=1000)),
                ('contentimage', models.FileField(upload_to='coursecontent')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.course')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.faculty')),
            ],
            options={
                'db_table': 'coursecontent_table',
            },
        ),
    ]
