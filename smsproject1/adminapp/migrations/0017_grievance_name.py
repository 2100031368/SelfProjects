# Generated by Django 5.0 on 2024-07-02 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0016_grievance_solved_grievance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='grievance',
            name='name',
            field=models.CharField(default=''),
        ),
    ]