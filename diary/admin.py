from django.contrib import admin
from .models import Weather, Emotion, Diary

# Register your models here.
admin.site.register(Weather)
admin.site.register(Emotion)
admin.site.register(Diary)
