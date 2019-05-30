from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<image_id>\d{0,50})$', views.main_view, name='main'),
    url(r'^post/$', views.upload_view, name='add_post')
]
