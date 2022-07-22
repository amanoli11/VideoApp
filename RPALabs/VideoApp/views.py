import json
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Video
from django.http import Http404
from .forms import FilterForm, PriceForm, VideoForPrice, VideoForm
from .validation import file_format_validation, file_length_validation, file_size_validation

from moviepy.editor import VideoFileClip
import datetime

# Create your views here.


def upload(request):

    # gives the object of last record in database
    lastvideo = Video.objects.last()
    form = VideoForm(request.POST or None, request.FILES or None)

    context = {'form': form, 'lastvideo': lastvideo}

    if form.is_valid():

        # get the name of the file uploaded
        video = request.FILES['video']
        video_name = str(video)

        # file_format_validation() checks if the file contains the extension of mp4 or mkv
        file_format = file_format_validation(video_name)
        file_size = file_size_validation(video.size)

        if file_format == True:
            # getting the duration of the video clip in seconds.
            file_length = VideoFileClip(video.temporary_file_path()).duration
            is_file_len_valid = file_length_validation(file_length)
        else:
            is_file_len_valid = None

        # validating the inputs.
        for i in [file_format, file_size, is_file_len_valid]:
            if i != True:
                context['error'] = True
                context['errormsg'] = i
                context['type'] = 'save'
                return render(request, 'UploadVideos.html', context)

        file_size_in_bytes = video.size
        file_size_in_mega_bytes = round(file_size_in_bytes/1024/1024, 2)
        form.instance.video_size_in_mb = float(file_size_in_mega_bytes)

        file_length = video
        file_length_in_seconds = VideoFileClip(
            file_length.temporary_file_path()).duration
        form.instance.video_length = str(
            datetime.timedelta(seconds=file_length_in_seconds))

        form.save()

        return redirect('upload-page')

    # Fetching all the values from database in decending format.
    all_videos = Video.objects.all().order_by('-id')
    return render(request, 'UploadVideos.html', {'context': context, 'list_videos': all_videos, 'type': 'save', 'form': context['form']})


def update_content(request, videoId):

    # get values from database according to id
    # get throws an error if no value is found. we use get() when we want to get single value.
    # if the id is invalid we send HttpResponse
    try:
        get_details = Video.objects.get(id=videoId)
    except Exception as e:
        return HttpResponse("ID does not exists")

    lastvideo = get_details

    # instance is used to get the values and set it into the form
    form = VideoForm(request.POST or None,
                     request.FILES or None, instance=get_details)
    context = {'form': form, 'lastvideo': lastvideo}

    if form.is_valid():

        new_file_chosen = request.FILES.get('video', False)

        # check if new file is chosen
        if new_file_chosen:
            video = request.FILES['video']
            video_name = str(video)

            # file_format_validation() checks if the file contains the extension of mp4 or mkv
            file_format = file_format_validation(video_name)
            file_size = file_size_validation(video.size)

            if file_format == True:
                # getting the duration of the video clip in seconds.
                file_length = VideoFileClip(
                    video.temporary_file_path()).duration
                is_file_len_valid = file_length_validation(file_length)
            else:
                is_file_len_valid = None

            # validating the inputs.
            for i in [file_format, file_size, is_file_len_valid]:
                if i != True:
                    context['error'] = True
                    context['errormsg'] = i
                    context['type'] = 'update'
                    return render(request, 'UploadVideos.html', context)

            file_size_in_bytes = video.size
            file_size_in_mega_bytes = round(file_size_in_bytes/1024/1024, 2)
            form.instance.video_size_in_mb = float(file_size_in_mega_bytes)

            file_length = video
            file_length_in_seconds = VideoFileClip(
                file_length.temporary_file_path()).duration
            form.instance.video_length = str(
                datetime.timedelta(seconds=file_length_in_seconds))

            form.save()
            return redirect('list-video')
        
        else:
            form.save()
            return redirect('list-video')

    return render(request, 'UploadVideos.html', {'context': context, 'type': 'update', 'form': form})


def dynamic_content(request, videoId):
    try:
        all_videos = Video.objects.get(id=videoId)
    except:
        return HttpResponse(json.dumps({"message": "Invalid ID"}))
    return render(request, 'Video.html', {'videoName': all_videos.name, "videoLocation": all_videos.video})


def dynamic_content_url(request, videoId):
    try:
        all_videos = Video.objects.get(id=videoId)
        video_relative_path = all_videos.video
        video_url = 'http://'+request.get_host()+'/media/'+str(video_relative_path)
    except:
        return HttpResponse(json.dumps({"message": "Invalid ID"}))
    return HttpResponse(json.dumps({"video_name": str(all_videos.name), "video_url": video_url}))


def list_videos(request, filter_name="None", format="asc"):
    try:
        if filter_name in ["name", "video_size_in_mb", "video_length", "created_date"]:
            if format == 'desc':
                all_videos = Video.objects.all().order_by('-'+filter_name)
            else:
                all_videos = Video.objects.all().order_by(filter_name)

            return render(request, 'ListVideos.html', {'list_videos': all_videos})

    except Exception as e:
        return HttpResponse("Please Enter valid URL")


def delete_content(request, deleteId):

    if request.method == "DELETE":

        try:
            value = Video.objects.get(id=deleteId)

            if value.count() == 0:
                return JsonResponse({'message': 'File does not exists'})

            value.delete()
            return HttpResponse("DELETED")

        except Exception as e:
            return HttpResponse("ID does not exists")

    try:
        video = Video.objects.get(id=deleteId)
        video.delete()
        return redirect('list-video')
    except:
        return HttpResponse("Please enter a valid Id")


def price(request):

    form = VideoForPrice(request.FILES or None)

    context = {
        'form': form
    }

    if request.method == "GET":
        return render(request, 'Price.html', {'form': form})

    if request.method == "POST":
        new_file_chosen = request.FILES.get('video', False)

        if new_file_chosen:
            video = request.FILES['video']
            video_name = str(video)

            # file_format_validation() checks if the file contains the extension of mp4 or mkv
            file_format = file_format_validation(video_name)
            file_size = file_size_validation(video.size)

            if file_format == True:
                # getting the duration of the video clip in seconds.
                file_length = VideoFileClip(video.temporary_file_path()).duration
                is_file_len_valid = file_length_validation(file_length)
            else:
                is_file_len_valid = None

            # validating the inputs.
            for i in [file_format, file_size, is_file_len_valid]:
                if i != True:
                    context['error'] = True
                    context['errormsg'] = i
                    return render(request, 'Price.html', context)

            file_size_in_bytes = request.FILES['video'].size
            file_size_in_mega_bytes = round(file_size_in_bytes/1024/1024, 2)
            file_size_in_mega_bytes = float(file_size_in_mega_bytes)

            file_length = request.FILES['video']
            file_length_in_seconds = VideoFileClip(file_length.temporary_file_path()).duration
            

            length = int(file_length_in_seconds)
            size = int(file_size_in_mega_bytes)
            price = 0

            if(size < 500):
                price = 5
            elif(size > 500):
                price = 12.5

            if(length < 378):
                price += 12.5
            elif(length > 378):
                price += 20

            return render(request, 'Price.html', {'form': form, "price": price})


def list_video_respond(request):
    form = FilterForm(request.POST)

    context = {
        'form': form
    }

    if form.is_valid():

        # for applying filters in rows
        if form.cleaned_data['filter_by'] == 'size' and form.cleaned_data['display_format'] == 'asc':
            all_videos = Video.objects.filter(video_size_in_mb__gte=float(
                form.cleaned_data['value'])).order_by('id')

        if form.cleaned_data['filter_by'] == 'size' and form.cleaned_data['display_format'] == 'desc':
            all_videos = Video.objects.filter(video_size_in_mb__gte=float(
                form.cleaned_data['value'])).order_by('-id')

        if form.cleaned_data['filter_by'] == 'name' and form.cleaned_data['display_format'] == 'asc':
            all_videos = Video.objects.filter(
                name__contains=form.cleaned_data['value']).order_by('id')

        if form.cleaned_data['filter_by'] == 'name' and form.cleaned_data['display_format'] == 'desc':
            all_videos = Video.objects.filter(
                name__contains=form.cleaned_data['value']).order_by('-id')

        return render(request, 'ListVideosRespond.html', {'context': context, 'list_videos': all_videos})

    # list all the records in descending order.
    all_videos = Video.objects.all().order_by('-id')
    context['list_videos'] = all_videos
    return render(request, 'ListVideosRespond.html', {'context': context, 'list_videos': all_videos})


def price_with_form(request):
    form = PriceForm(request.POST)

    # getting values from the form.
    if form.is_valid():
        size = form.cleaned_data['size_in_mb']
        vid_min = form.cleaned_data['video_length_min']
        vid_sec = form.cleaned_data['video_length_sec']
        format = form.cleaned_data['video_type']

        price = 0
        error = False
        errormessage = ''

        if(size >= 500):
            price = 12.5
        elif(size < 500):
            price = 5

        total_duration = vid_min*60+vid_sec

        if(total_duration >= 378):
            price += 20
        elif(total_duration < 378):
            price += 12.5

        if format not in ["mp4", "mkv"]:
            error = True,
            errormessage = "Please select a format of MP4 or MKV."

        return render(request, 'GetPriceWithInput.html', {'form': form, 'error': error, 'errormessage': errormessage, 'price': price})

    return render(request, 'GetPriceWithInput.html', {'form': form, 'price': 0})
