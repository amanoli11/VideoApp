from django.urls import path, include
from .views import delete_content, dynamic_content_url, list_video_respond, list_videos, price, price_with_form, update_content, upload
from .views import dynamic_content

urlpatterns = [
    path('', upload, name="upload-page"),
    # path('video', dynamic_content)
    path('video/<int:videoId>/', dynamic_content),
    path('video/url/<int:videoId>/', dynamic_content_url),
    path('video/update/<int:videoId>/', update_content, name="update"),
    path('video/delete/<int:deleteId>/', delete_content, name="delete-content"),
    path('video/list/respond', list_video_respond, name="list-video"),
    path('video/list/<filter_name>/<format>', list_videos),
    path('price', price, name="get-price"),
    path('price/forms', price_with_form, name="price-form"),
    # path(r'^video/list/(?P<product>\w+)/$', list_videos),

]