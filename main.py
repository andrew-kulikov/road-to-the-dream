import argparse
from src import Task, TaskList, Controller, BasicConnector
from src.tools import parsers


def login(args):
    login_ = args.login
    password = args.password
    try:
        application.authorize(login_, password)
        print('Authorized successfully')
    except KeyError as e:
        print(e)


def register(args):
    login_ = args.login
    password = args.password
    name = args.name
    try:
        application.register_user(name, login_, password)
        print('Registered successfully')
    except KeyError as e:
        print(e)


def print_all_users(args=None):
    controller = Controller()
    users = controller.get_all_users()
    for user in users:
        print(user)


def print_user(args=None):
    print(application.cur_user)


def add_task(args):
    name = args.name
    tags = args.tags
    description = args.description
    parent_id = args.parent
    priority = args.priority
    deadline = args.deadline
    period = args.period
    try:
        controller = Controller()
        task = Task(title=name, tags=tags, description=description,
                    parent_id=parent_id, priority=priority, period_val=period,
                    deadline=to)
        controller.add_task(task)
        #application.add_task(name, description, tags, priority, parent_id, deadline, period)
        print('Added successfully')
    except Exception as e:
        print(e)


def edit_task(args):
    name = args.name
    tags = args.tags
    task_id = args.id
    description = args.description
    priority = args.priority
    deadline = args.deadline
    period = args.period
    try:
        application.edit_task(task_id=task_id, name=name, description=description, tags=tags,
                              priority=priority, deadline=deadline, period=period)
        print('Edited successfully')
    except Exception as e:
        print(e)


def complete_task(args):
    task_id = args.id
    try:
        controller = Controller()
        controller.complete_task(task_id)
        print('Completed successfully')
    except Exception as e:
        print(e)


def remove_task(args):
    task_id = int(args.id)
    try:
        controller = Controller()
        controller.delete_task(task_id)
        print('Removed successfully')
    except Exception as e:
        print(e)


def move_task(args):
    source = args.source
    dest = args.destination
    try:
        application.move_task(source, dest)
        print('Moved successfully')
    except Exception as e:
        print(e)


def add_project(args):
    name = args.name
    private = args.private
    try:
        controller = Controller()
        task_list = TaskList(name=name, is_private=private)
        controller.add_task_list(task_list)
        print('Task list created successfully')
    except Exception as e:
        print(e)


def edit_project_task(args):
    project_id = args.project_id
    task_id = args.id
    name = args.name
    tags = args.tags
    description = args.description
    priority = args.priority
    deadline = args.deadline
    period = args.period
    try:
        application.edit_project_task(task_id, name, description, tags, deadline=deadline,
                                      priority=priority, project_id=project_id, period=period)
        print('Edited successfully')
    except Exception as e:
        print(e)


def complete_project_task(args):
    project_id = args.project_id
    task_id = args.task_id
    try:
        application.complete_project_task(task_id, project_id)
        print('Completed successfully')
    except Exception as e:
        print(e)


def print_tasks(args):
    mode = 'pending'
    if args.completed:
        mode = 'completed'
    elif args.failed:
        mode = 'failed'
    try:
        controller = Controller()
        for task in controller.get_all_tasks():
            if task.status == mode:
                print(task)
    except AttributeError as e:
        print(e)


def inspect_task(args):
    task_id = args.id
    print(application.get_full_task_info(task_id))


def print_project_tasks(args):
    mode = 'pending'
    id = args.project_id
    if args.completed:
        mode = 'completed'
    elif args.failed:
        mode = 'failed'
    try:
        for task in application.get_project_task_list(mode, id):
            print(task)
    except Exception as e:
        print(e)


def print_project_users(args):
    project_id = args.project_id
    for user in application.get_project_users(project_id):
        print(user)


def print_projects(args):
    for project in application.get_projects():
        print(project)
        print('-'*20)


def open_project(args):
    id = args.project_id
    try:
        application.load_project(id)
        print('Project loaded')
    except Exception as e:
        print(e)


def sort_tasks(args):
    mode = ''
    if args.title:
        mode = 'title'
    elif args.date:
        mode = 'deadline'
    elif args.priority:
        mode = 'priority'
    try:
        controller = Controller()
        controller.sort_tasks(mode)
        print('Task sorted successfully')
    except Exception as e:
        print(e)


def parse_args():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-command help')

    users_parser = subparsers.add_parser('users', help='Log in or watch users')

    user_subparsers = users_parser.add_subparsers(help='sub-command help')

    login_parser = user_subparsers.add_parser('login', help='Log in the system')
    login_parser.add_argument('-l', '--login', help='Your login', default='vasya')
    login_parser.add_argument('-p', '--password', help='Your password', default='123')
    login_parser.set_defaults(func=login)

    register_parser = user_subparsers.add_parser('register', help='Register in the system')
    register_parser.add_argument('-l', '--login', help='Your login', default='vasya', required=True)
    register_parser.add_argument('-p', '--password', help='Your password', default='123', required=True)
    register_parser.add_argument('-n', '--name', help='Your name', default='vasya', required=True)
    register_parser.set_defaults(func=register)

    list_parser = user_subparsers.add_parser('who', help='List all users')
    list_parser.set_defaults(func=print_all_users)
    who_parser = user_subparsers.add_parser('whoami', help='Display logged user')
    who_parser.set_defaults(func=print_user)

    add_parser = subparsers.add_parser('add', help='Add task to your task list')
    add_parser.add_argument('-n', '--name', help='Task name', default='Simple task', required=True)
    add_parser.add_argument('-d', '--description', help='Task description', default='', required=False)
    add_parser.add_argument('-t', '--tags', help='Task tags', nargs='+', required=False)
    add_parser.add_argument('-r', '--priority', type=int, help='Task priority (0-9). 0 - highest priority', default=0)
    add_parser.add_argument('-p', '--parent', help='ID of parent task', default=0)
    add_parser.add_argument('-e', '--deadline', help='Date of deadline in format [DD.MM.YYYY HH:MM]', default=None)
    add_parser.add_argument('-pe', '--period',
                            help='Period of repeating in format d - day; w - week; m - month; y - year', default=None)
    add_parser.set_defaults(func=add_task)

    edit_parser = subparsers.add_parser('edit', help='Edit task with selected id')
    edit_parser.add_argument('-i', '--id', help='Task id', default=0)
    edit_parser.add_argument('-n', '--name', help='New task name', default=None)
    edit_parser.add_argument('-d', '--description', help='New task description', default=None)
    edit_parser.add_argument('-t', '--tags', help='New task tags', nargs='+', default=None)
    edit_parser.add_argument('-r', '--priority', type=int,
                             help='New task priority (0-9). 0 - highest priority', default=None)
    edit_parser.add_argument('-e', '--deadline',
                             help='New deadline of deadline in format [DD.MM.YYYY HH:MM]', default=None)
    edit_parser.add_argument('-pe', '--period', default=None,
                             help='New period of repeating in format d - day; w - week; m - month; y - year')
    edit_parser.set_defaults(func=edit_task)

    complete_parser = subparsers.add_parser('complete', help='Complete task #ID')
    complete_parser.add_argument('id', help='Id of completed task')
    complete_parser.set_defaults(func=complete_task)

    remove_parser = subparsers.add_parser('remove', help='Remove task #ID')
    remove_parser.add_argument('id', help='Id of task to remove')
    remove_parser.set_defaults(func=remove_task)

    move_parser = subparsers.add_parser('move', help='Move task #source to sub tasks of task #destination')
    move_parser.add_argument('-s', '--source', help='Id of parent task', required=True)
    move_parser.add_argument('-d', '--destination', help='Id of task you want to move', required=True)
    move_parser.set_defaults(func=move_task)

    task_list_parser = subparsers.add_parser('list', help='Print all your tasks')
    print_group = task_list_parser.add_mutually_exclusive_group()
    print_group.add_argument('-p', '--pending', action='store_true', help='Print all pending tasks')
    print_group.add_argument('-c', '--completed', action='store_true', help='Print all completed tasks')
    print_group.add_argument('-f', '--failed', action='store_true', help='Print all failed tasks')
    task_list_parser.set_defaults(func=print_tasks)

    task_sort_parser = subparsers.add_parser('sort', help='Sort tasks in specific order')
    sort_group = task_sort_parser.add_mutually_exclusive_group()
    sort_group.add_argument('-t', '--title', action='store_true', help='Sort tasks by name')
    sort_group.add_argument('-d', '--deadline', action='store_true', help='Sort tasks by deadline')
    sort_group.add_argument('-p', '--priority', action='store_true', help='Sort tasks by priority')
    task_sort_parser.set_defaults(func=sort_tasks)

    more_parser = subparsers.add_parser('more', help='Show full information of task #ID')
    more_parser.add_argument('id', help='Id of task to inspect')
    more_parser.set_defaults(func=inspect_task)

    projects_parser = subparsers.add_parser('project', help='Manage projects')

    project_subparsers = projects_parser.add_subparsers(help='sub-command help')

    project_add_parser = project_subparsers.add_parser('open', help='Open new project')
    project_add_parser.add_argument('project_id', help='Project id')
    project_add_parser.set_defaults(func=open_project)

    project_open_parser = project_subparsers.add_parser('create', help='Create new project')
    project_open_parser.add_argument('-n', '--name', help='Project name', default='Simple project', required=True)
    project_open_parser.set_defaults(func=add_project)

    project_task_list_parser = project_subparsers.add_parser('list_tasks', help='Print tasks in project #id')
    project_task_list_parser.add_argument('-pi', '--project_id', help='Project id', default=0)
    project_print_group = project_task_list_parser.add_mutually_exclusive_group()
    project_print_group.add_argument('-p', '--pending', action='store_true', help='Print all pending tasks')
    project_print_group.add_argument('-c', '--completed', action='store_true', help='Print all completed tasks')
    project_print_group.add_argument('-f', '--failed', action='store_true', help='Print all failed tasks')
    project_task_list_parser.set_defaults(func=print_project_tasks)

    project_list_parser = project_subparsers.add_parser('list', help='Print all projects')
    project_list_parser.set_defaults(func=print_projects)

    """
    project_task_sort_parser = project_subparsers.add_parser('sort', help='Sort project tasks in specific order')
    project_sort_group = project_task_sort_parser.add_mutually_exclusive_group()
    project_sort_group.add_argument('-n', '--name', action='store_true', help='Sort tasks by name')
    project_sort_group.add_argument('-d', '--deadline', action='store_true', help='Sort tasks by deadline')
    project_sort_group.add_argument('-p', '--priority', action='store_true', help='Sort tasks by priority')
    project_task_sort_parser.set_defaults(func=sort_project_tasks)
    """

    project_users_parser = project_subparsers.add_parser('users', help='Print all users in project')
    project_users_parser.add_argument('-pi', '--project_id', help='Project id', default=0)
    project_users_parser.set_defaults(func=print_project_users)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)


def main():
    parse_args()


if __name__ == '__main__':
    application = None
    main()
