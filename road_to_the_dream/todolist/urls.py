from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<task_id>\w{0,50})/$', views.details),
    url(r'^lists/add/$', views.add_list),
    url(r'^lists/completed/$', views.completed),
    url(r'^lists/trash/$', views.trash),
    url(r'^lists/(?P<list_id>\w{0,50})/$', views.list_details),
    url(r'^tags/(?P<tag_id>\w{0,50})/$', views.tag_details),
    url(r'^edit/(?P<task_id>\w{0,50})/$', views.edit_task),
    url(r'^trash/(?P<task_id>\w{0,50})/$', views.trash_task),
    url(r'^delete/(?P<task_id>\w{0,50})/$', views.delete_task),
    url(r'^complete/(?P<task_id>\w{0,50})/$', views.complete_task),
    url(r'^repair/(?P<task_id>\w{0,50})/$', views.repair_task),
    url(r'^add/$', views.add, name='add')
]
