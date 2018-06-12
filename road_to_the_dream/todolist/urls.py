from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<task_id>\w{0,50})/$', views.details),
    url(r'^lists/add/$', views.add_list),
    url(r'^lists/(?P<list_id>\w{0,50})/$', views.list_details),
    url(r'^tags/(?P<tag_id>\w{0,50})/$', views.tag_details),
    url(r'^add/$', views.add, name='add')
]
