from django.contrib import admin

from .models import  Admin,Faculty, Course, Student, FacultyCourseMapping

# Register your models here.
admin.site.register(Admin)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(FacultyCourseMapping)