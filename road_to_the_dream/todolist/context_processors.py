from .models import TaskList, Tag


def add_variable_to_context(request):
    tasklists = None
    tags = None
    if not request.user.is_anonymous:
        tasklists = TaskList.objects.filter(users__in=[request.user])
        tags = Tag.objects.filter(users__in=[request.user])
    return {
        'task_lists': tasklists,
        'tags': tags,
        'user': request.user,
        'request_path': request.path,
    }
