# Generated by Django 5.0 on 2024-06-22 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0007_alter_faculty_facultyid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultycoursemapping',
            name='component',
        ),
    ]