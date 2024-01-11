# Generated by Django 5.0 on 2024-01-05 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regapp', '0004_reghistorym_sec1_reghistorym_sec2_reghistorym_sec3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackPosted',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sid', models.CharField()),
                ('sname', models.CharField()),
                ('sprogram', models.CharField()),
                ('sdept', models.CharField()),
                ('say', models.CharField()),
                ('syr', models.IntegerField()),
                ('ssem', models.CharField()),
                ('ccode', models.CharField()),
                ('ctitle', models.CharField()),
                ('faculty', models.BigIntegerField()),
                ('section', models.IntegerField()),
                ('q1', models.CharField(default='Is the syllabus coverage matching with the lesson plan as on date?', max_length=1000)),
                ('fdb1', models.CharField(choices=[('100% Matching', '100% Matching'), ('Almost Matching', 'Almost Matching'), ('Moderate', 'Moderate'), ('Not at all', 'Not at all')])),
                ('q2', models.CharField(default='How well is the teacher able to explain the concept?', max_length=100)),
                ('fdb2', models.CharField(choices=[('Excellent ', 'Excellent '), ('Very Good', 'Very Good'), ('Good', 'Good'), ('Satisfactory ', 'Satisfactory '), ('Not-Satisfactory', 'Not-Satisfactory')])),
                ('q3', models.CharField(default='Is the teacher encouraging interaction to get the doubts clarified?', max_length=100)),
                ('fdb3', models.CharField(choices=[('Excellent ', 'Excellent '), ('Very Good', 'Very Good'), ('Good', 'Good'), ('Satisfactory ', 'Satisfactory '), ('Not-Satisfactory', 'Not-Satisfactory')])),
                ('q4', models.CharField(default='Whether your teacher is teaching in any other language than English?', max_length=100)),
                ('fdb4', models.CharField(choices=[('Never', 'Never'), ('Very Rare', 'Very Rare'), ('Less frequently', ' Less frequently'), ('More frequently', 'More frequently'), ('All the time', 'All the time')])),
                ('q5', models.CharField(default='Overall rating of your teacher.', max_length=100)),
                ('fdb5', models.CharField(choices=[('Excellent ', 'Excellent '), ('Very Good', 'Very Good'), ('Good', 'Good'), ('Satisfactory ', 'Satisfactory '), ('Not-Satisfactory', 'Not-Satisfactory')])),
            ],
            options={
                'db_table': 'feedback_posted',
            },
        ),
    ]