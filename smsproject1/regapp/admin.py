from django.contrib import admin

# Register your models here.
from .models import RegHistoryM, RegM, FeedbackPosted

admin.site.register(RegHistoryM)
admin.site.register(RegM)
admin.site.register(FeedbackPosted)