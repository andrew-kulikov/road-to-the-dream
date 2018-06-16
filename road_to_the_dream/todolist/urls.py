from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<task_id>\d{1,50})/$', views.details),
    url(r'^subtasks/(?P<subtask_id>\w{0,50})/complete/$', views.complete_subtask),
    url(r'^subtasks/(?P<subtask_id>\w{0,50})/delete/$', views.delete_subtask),
    url(r'^subtasks/(?P<subtask_id>\w{0,50})/repair/$', views.repair_subtask),
    url(r'^lists/add/$', views.add_list),
    url(r'^lists/completed/$', views.completed),
    url(r'^lists/trash/$', views.trash),
    url(r'^lists/today/$', views.today),
    url(r'^lists/next-week/$', views.next_week),
    url(r'^lists/(?P<list_id>\w{0,50})/$', views.list_details),
    url(r'^lists/(?P<list_id>\w{0,50})/edit/$', views.edit_list),
    url(r'^lists/(?P<list_id>\w{0,50})/delete/$', views.delete_list),
    url(r'^lists/(?P<list_id>\w{0,50})/invite/$', views.invite),
    url(r'^lists/(?P<list_id>\w{0,50})/kick/(?P<user_id>\w{0,50})/$', views.kick),
    url(r'^tags/add/$', views.add_tag),
    url(r'^tags/details/(?P<tag_id>\w{0,50})/$', views.tag_details),
    url(r'^edit/(?P<task_id>\w{0,50})/$', views.edit_task),
    url(r'^trash/(?P<task_id>\w{0,50})/$', views.trash_task),
    url(r'^delete/(?P<task_id>\w{0,50})/$', views.delete_task),
    url(r'^complete/(?P<task_id>\w{0,50})/$', views.complete_task),
    url(r'^repair/(?P<task_id>\w{0,50})/$', views.repair_task),
    url(r'^add/$', views.add, name='add')
]
