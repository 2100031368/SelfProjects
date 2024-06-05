from django.contrib import admin

from .models import CourseContent, CC, Internals, Handout

# Register your models here.

admin.site.register(CourseContent)
admin.site.register(CC)
admin.site.register(Internals)
admin.site.register(Handout)