import json
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Video
from django.http import Http404
from .forms import FilterForm, PriceForm, VideoForm
from .validation import file_format_validation, file_length_validation, file_size_validation

from moviepy.editor import VideoFileClip
import datetime

# Create your views here.

def upload(request):

    lastvideo = Video.objects.last()

    form = VideoForm(request.POST or None, request.FILES or None)
    
    context= {
            'form': form,
            'lastvideo': lastvideo,
            }

    if request.method == "GET":
        print('get get')
        all_videos = Video.objects.all().order_by('-id')
        count_rows = all_videos.count()
        context['list_videos'] = all_videos
        return render(request, 'UploadVideos.html', {'context': context, 'list_videos': all_videos, 'length': count_rows, 'type': 'save', 'form': context['form']})

    
    if request.method == "POST":
        print('im here')
        if form.is_valid():
            video_name = str(request.FILES['video'])

            file_format = file_format_validation(video_name)

            if file_format != True:
                context['error'] = True
                context['errormsg'] = file_format
                return render(request, 'UploadVideos.html', context)

            
            video_length = file_length_validation(request.FILES['video'])
            if video_length != True:
                context['error'] = True
                context['errormsg'] = video_length
                return render(request, 'UploadVideos.html', context)


            file_size = file_size_validation(request.FILES['video'].size)
            if file_size != True:
                context['error'] = True
                context['errormsg'] = file_size
                return render(request, 'UploadVideos.html', context)

            
            file_size_in_bytes = request.FILES['video'].size
            file_size_in_mega_bytes = round(file_size_in_bytes/1024/1024, 2)
            form.instance.video_size_in_mb = str(file_size_in_mega_bytes)


            file_length = request.FILES['video']
            file_length_in_seconds = VideoFileClip(file_length.temporary_file_path()).duration
            form.instance.video_length = str(datetime.timedelta(seconds=file_length_in_seconds))

            # all_videos = Video.objects.get(id = videoId)
            # video_relative_path = all_videos.video
            # form.instance.urls = 'http://127.0.0.1:8000/media/'+str(video_relative_path)

            # print(video_name.split('.')[1])

            # print(request.FILES['video'].size)

            # a = VideoFileClip(request.FILES['video'].temporary_file_path())
            # print(a.duration)

            # video_location = video_name
            # clip = VideoFileClip(request.FILES.get('video'))
            # print(clip.duration)
            # print(video_location)
            form.save()

        return redirect(request.path)



def update_content(request, videoId):

    # if request.method == "GET":
    get_details = Video.objects.get(id = videoId)
    list_all_videos = Video.objects.filter(id = videoId)
    # count_rows =  all_videos.count()

    context= {}
    form = VideoForm(request.POST or None, request.FILES or None, instance=get_details)

    if form.is_valid():
        new_file_chosen = request.FILES.get('video', False)
        
        if new_file_chosen:
            video_name = str(request.FILES['video'])

            file_format = file_format_validation(video_name)

            if file_format != True:
                context['error'] = True
                context['errormsg'] = file_format
                return render(request, 'UploadVideos.html', context)

            
            video_length = file_length_validation(request.FILES['video'])
            if video_length != True:
                context['error'] = True
                context['errormsg'] = video_length
                return render(request, 'UploadVideos.html', context)


            file_size = file_size_validation(request.FILES['video'].size)
            if file_size != True:
                context['error'] = True
                context['errormsg'] = file_size
                return render(request, 'UploadVideos.html', context)

            
            file_size_in_bytes = request.FILES['video'].size
            file_size_in_mega_bytes = round(file_size_in_bytes/1024/1024, 2)
            form.instance.video_size_in_mb = str(file_size_in_mega_bytes)

            file_length = request.FILES['video']
            file_length_in_seconds = VideoFileClip(file_length.temporary_file_path()).duration
            form.instance.video_length = str(datetime.timedelta(seconds=file_length_in_seconds))
        
        form.save()
        return redirect('upload-page')
    return render(request, 'UploadVideos.html', {'context': context, 'list_videos': list_all_videos, 'type': 'update', 'form': form})


    # obj = get_object_or_404(Video, id = videoId)
    # form = VideoForm(request.POST or None, request.FILES or None, instance = obj)
    
    # context= {
    #         'form': form
    #         }



    # if request.method == "PATCH":
    #     return HttpResponse("PATCH")

    # if request.method == "POST":

        # return HttpResponse('asdasd')

        # fetch the object related to passed id


        # if form.is_valid():

            # video_name = str(request.FILES['video'])
            # file_format = file_format_validation(video_name)

            # if file_format != True:
            #     context['error'] = True
            #     context['errormsg'] = file_format
            #     return render(request, 'UploadVideos.html', context)

            
            # video_length = file_length_validation(request.FILES['video'])
            # if video_length != True:
            #     context['error'] = True
            #     context['errormsg'] = video_length
            #     return render(request, 'UploadVideos.html', context)


            # file_size = file_size_validation(request.FILES['video'].size)
            # if file_size != True:
            #     context['error'] = True
            #     context['errormsg'] = file_size
            #     return render(request, 'UploadVideos.html', context)

            
            # file_size_in_bytes = request.FILES['video'].size
            # file_size_in_mega_bytes = round(file_size_in_bytes/1024/1024, 2)
            # form.instance.video_size = str(file_size_in_mega_bytes)+" MB"


            # file_length = request.FILES['video']
            # form.instance.video_length = str(VideoFileClip(file_length.temporary_file_path()).duration)+" Seconds"

            # form.save()

        # return HttpResponse('UPDATE')

        # return redirect('http://127.0.0.1:8000/')



def dynamic_content(request, videoId):

    try:
        all_videos = Video.objects.get(id = videoId)
    except Video.DoesNotExist:
        raise Http404

    return render(request, 'Video.html', {'videoName': all_videos.name, "videoLocation": all_videos.video})
    # video_list = Video.objects.all()
    # return HttpResponse(video_list)

def dynamic_content_url(request, videoId):

    try:
        all_videos = Video.objects.get(id = videoId)
        video_relative_path = all_videos.video
        video_url = 'http://127.0.0.1:8000/media/'+str(video_relative_path)
        # Video.objects.get(id = videoId)
        # return HttpResponse(json.dumps({"video_name": str(all_videos.name), "video_url": video_url}))
    except Video.DoesNotExist:
        raise Http404

    return HttpResponse(json.dumps({"video_name": str(all_videos.name), "video_url": video_url}))
    # print('http://127.0.0.1:8000/media/{%video_relative_path%}}')
    # return HttpResponse(json.dumps({'video_url': all_videos.video}))
    # print(all_videos.name, all_videos.video)
    # return render(request, 'Video.html', {'videoName': all_videos.name, "videoLocation": all_videos.video})


def list_videos(request, filter_name = "None", format = "asc"):
    
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
            value = Video.objects.filter(id=deleteId)
            
            if value.count() == 0:
                return JsonResponse({'message': 'File does not exists'})
                
            value.delete()
            return HttpResponse("DELETED")
        
        except Exception as e:
            return HttpResponse(e)


    Video.objects.filter(id=deleteId).delete()
    return redirect('upload-page')


def price(request):

    form = VideoForm(request.POST or None, request.FILES or None)
    
    context = {}

    if request.method == "GET":
        return render(request, 'Price.html', {'form': form})
        # all_videos = Video.objects.all().order_by('id')
        # count_rows = all_videos.count()
        return render(request, 'Price.html', {'form': form, "price": price })

    
    if request.method == "POST":
        if form.is_valid():
            video_name = str(request.FILES['video'])

            file_format = file_format_validation(video_name)

            if file_format != True:
                context['error'] = True
                context['errormsg'] = file_format
                context['form'] = form
                return render(request, 'Price.html', context)

            
            print('im here')
            video_length = file_length_validation(request.FILES['video'])
            if video_length != True:
                context['error'] = True
                context['errormsg'] = video_length
                return render(request, 'Price.html', context)


            file_size = file_size_validation(request.FILES['video'].size)
            if file_size != True:
                context['error'] = True
                context['errormsg'] = file_size
                return render(request, 'Price.html', context)

            
            file_size_in_bytes = request.FILES['video'].size
            file_size_in_mega_bytes = round(file_size_in_bytes/1024/1024, 2)
            form.instance.video_size = str(file_size_in_mega_bytes)


            file_length = request.FILES['video']
            file_length_in_seconds = VideoFileClip(file_length.temporary_file_path()).duration
            form.instance.video_length = str(datetime.timedelta(seconds=file_length_in_seconds))

            # form.save()

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

        return render(request, 'Price.html', {'form': form, "price": price })
        return redirect(request.path)


def list_video_respond(request):
    form = FilterForm(request.POST)

    context = {
        'form': form
    }

    if form.is_valid():
        print(form.cleaned_data['value'])
        
        if form.cleaned_data['filter_by'] == 'size' and form.cleaned_data['display_format'] == 'asc':
            all_videos = Video.objects.filter(video_size_in_mb__gte = float(form.cleaned_data['value'])).order_by('id')
        
        if form.cleaned_data['filter_by'] == 'size' and form.cleaned_data['display_format'] == 'desc':
            all_videos = Video.objects.filter(video_size_in_mb__gte = float(form.cleaned_data['value'])).order_by('-id')


        if form.cleaned_data['filter_by'] == 'name' and form.cleaned_data['display_format'] == 'asc':
            all_videos = Video.objects.filter(name__contains = form.cleaned_data['value']).order_by('id')

        if form.cleaned_data['filter_by'] == 'name' and form.cleaned_data['display_format'] == 'desc':
            all_videos = Video.objects.filter(name__contains = form.cleaned_data['value']).order_by('-id')

        return render(request, 'ListVideosRespond.html', {'context': context, 'list_videos': all_videos})
        
    all_videos = Video.objects.all().order_by('-id')
    count_rows = all_videos.count()
    context['list_videos'] = all_videos
    return render(request, 'ListVideosRespond.html', {'context': context, 'list_videos': all_videos, 'length': count_rows, 'type': 'save'})



def price_with_form(request):
    form = PriceForm(request.POST)
    # print(request.POST)
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