from django.db import models
from .models import Video
from django.forms import ModelForm
from django import forms


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["name", "video"]


class PriceForm(forms.Form):
    size_in_mb = forms.FloatField()
    video_length_min = forms.IntegerField()
    video_length_sec = forms.IntegerField()
    video_type = forms.CharField(max_length=20)


class FilterForm(forms.Form):
    filter_choices =(
        ("size", "Video Size"),
        ("name", "Video Name"),
    )

    format =(
        ("asc", "Ascending"),
        ("desc", "Descending")
    )

    filter_by = forms.ChoiceField(choices=filter_choices, initial='size')
    value = forms.CharField(max_length=255)
    display_format = forms.ChoiceField(choices=format, initial='asc')

    # size = forms.IntegerField(required=False)
    # min_length = forms.IntegerField(required=False)
    # max_length = forms.IntegerField(required=False)
    # format = forms.ComboField()