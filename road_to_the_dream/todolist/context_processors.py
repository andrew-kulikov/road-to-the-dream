from .models import TaskList, Tag


def add_variable_to_context(request):
    return {
        'task_lists': TaskList.objects.all(),
        'tags': Tag.objects.all(),
        'user': request.user,
    }
