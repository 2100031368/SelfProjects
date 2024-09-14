from django.contrib import admin

from .models import CourseContent,InternalsAccess, Internals, Handout

# Register your models here.

admin.site.register(CourseContent)
admin.site.register(InternalsAccess)
admin.site.register(Internals)
admin.site.register(Handout)