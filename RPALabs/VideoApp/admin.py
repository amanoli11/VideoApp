from django.contrib import admin
from .models import Video
# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'video')
    readonly_fields: ('created_date')

admin.site.register(Video, VideoAdmin)