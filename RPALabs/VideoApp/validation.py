from moviepy.editor import VideoFileClip
import os
import datetime

def file_format_validation(file_name):
    
    # file_name = 'Toy.Story.3.2010.1080p.BRrip.x264.YIFY.srt'
    # print(os.path.splitext(file_name))

    file_format = os.path.splitext(file_name)[1]

    available_formats = [".mp4", ".mkv"]

    if file_format in available_formats:
        return True
    else:
        return "Only .MP4 and .MKV are supported."


def file_length_validation(file):

    # clip = VideoFileClip(request.FILES.get('video'))
            # print(clip.duration)
    
    file_length = VideoFileClip(file.temporary_file_path())

    if file_length.duration < 600:
        return True
    else:
        return "The length of the file should be less than 10 minutes."


def file_size_validation(size):
    
    if size < 1073741824:
        return True
    else:
        return "The size of the file cannot be greated than 1000 MB."