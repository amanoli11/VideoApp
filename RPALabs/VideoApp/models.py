from django.db import models
from django.contrib import admin
from datetime import datetime, date
# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    video_size_in_mb = models.FloatField(editable=False, null=True)
    video_length = models.TextField(editable=False, null=True)