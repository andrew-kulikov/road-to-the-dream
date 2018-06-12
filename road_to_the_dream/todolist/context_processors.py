from .models import TaskList, Tag


def add_variable_to_context(request):
    return {
        'task_lists': TaskList.objects.filter(users__in=[request.user]),
        'tags': Tag.objects.all(),
        'user': request.user,
        'request_path': request.path,
    }
