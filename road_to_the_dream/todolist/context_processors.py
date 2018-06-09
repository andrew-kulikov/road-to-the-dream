from .models import TaskList


def add_variable_to_context(request):
    return {
        'task_lists': TaskList.objects.all()
    }
