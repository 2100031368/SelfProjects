from django.db import models

# Create your models here.
from adminapp.models import Faculty, Course

class CourseContent(models.Model):
    id=models.AutoField(primary_key=True)
    faculty=models.ForeignKey(Faculty, blank=False, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, blank=False, on_delete=models.CASCADE)
    description=models.TextField(max_length=1000, blank=False)
    link=models.CharField(max_length=1000)
    contentimage=models.FileField(blank=False, upload_to='coursecontent/')

    class Meta:
        db_table="coursecontent_table"

class CC(models.Model):
    id = models.AutoField(primary_key=True)
    fid = models.BigIntegerField(blank=False)
    cc = models.CharField(blank=False)
    ay = models.CharField(blank=False, max_length=100)
    yr=models.IntegerField(blank=False)
    sem=models.CharField(blank=False)

    post=models.IntegerField(blank=False, default=0)


class Internals(models.Model):
    id = models.AutoField(primary_key=True)
    fid=models.BigIntegerField(blank=False)
    sid=models.CharField(blank=False)
    dept = models.CharField(blank=False, max_length=200)
    ay=models.CharField(blank=False, max_length=100)
    yr=models.IntegerField(blank=False)
    sem=models.CharField(blank=False, max_length=50)
    cid=models.IntegerField(blank=False)
    cc=models.CharField(blank=False, max_length=50)
    sec=models.IntegerField(blank=False)
    sem1=models.FloatField()
    sem2=models.FloatField()
    lab1=models.FloatField()
    quiz1 = models.FloatField()
    quiz2 = models.FloatField()
    quiz3 = models.FloatField()
    quiz4 = models.FloatField()
    semend = models.FloatField()
    labend = models.FloatField()
    grade_points = models.FloatField()
    grade = models.CharField(default="F")

    class Meta:
        db_table = "internals_table"

