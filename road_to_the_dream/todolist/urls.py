from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<task_id>\d{1,50})/$', views.details, name='details'),
    url(r'^subtasks/(?P<subtask_id>\d{0,50})/complete/$', views.complete_subtask, name='complete_subtask'),
    url(r'^subtasks/(?P<subtask_id>\d{0,50})/delete/$', views.delete_subtask, name='delete_subtask'),
    url(r'^subtasks/(?P<subtask_id>\d{0,50})/repair/$', views.repair_subtask, name='repair_subtask'),
    url(r'^lists/add/$', views.add_list, name='add_list'),
    url(r'^lists/completed/$', views.completed, name='completed'),
    url(r'^lists/trash/$', views.trash, name='trash'),
    url(r'^lists/today/$', views.today, name='today'),
    url(r'^lists/next-week/$', views.next_week, name='next_week'),
    url(r'^lists/(?P<list_id>\d{0,50})/$', views.list_details, name='list_details'),
    url(r'^lists/(?P<list_id>\d{0,50})/edit/$', views.edit_list, name='edit_list'),
    url(r'^lists/(?P<list_id>\d{0,50})/delete/$', views.delete_list, name='delete_list'),
    url(r'^lists/(?P<list_id>\d{0,50})/invite/$', views.invite, name='invite'),
    url(r'^lists/(?P<list_id>\d{0,50})/kick/(?P<user_id>\d{0,50})/$', views.kick, name='kick_user'),
    url(r'^tags/add/$', views.add_tag, name='add_tag'),
    url(r'^tags/details/(?P<tag_id>\d{0,50})/$', views.tag_details, name='tag_details'),
    url(r'^edit/(?P<task_id>\d{0,50})/$', views.edit_task, name='edit_task'),
    url(r'^trash/(?P<task_id>\d{0,50})/$', views.trash_task, name='trash_task'),
    url(r'^delete/(?P<task_id>\d{0,50})/$', views.delete_task, name='delete_task'),
    url(r'^complete/(?P<task_id>\d{0,50})/$', views.complete_task, name='complete_task'),
    url(r'^repair/(?P<task_id>\d{0,50})/$', views.repair_task, name='repair_task'),
    url(r'^add/$', views.add, name='add')
]
