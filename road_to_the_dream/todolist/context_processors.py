from .models import TaskList, Tag


def add_variable_to_context(request):
    tasklists = None
    if not request.user.is_anonymous:
        tasklists = TaskList.objects.filter(users__in=[request.user])
    return {
        'task_lists': tasklists,
        'tags': Tag.objects.filter(users__in=[request.user]),
        'user': request.user,
        'request_path': request.path,
    }
