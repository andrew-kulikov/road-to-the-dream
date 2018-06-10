from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url('^signup/$', views.signup, name='signup'),
    url('^login/$', views.login_view),
    url(r'^logout/$', views.log_out, name='logout')
]
