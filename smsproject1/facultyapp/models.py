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