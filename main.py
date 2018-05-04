from src import Task, TaskList, User, Application
import argparse
import jsonpickle


def login(args):
    login_ = args.login
    password = args.password
    try:
        Application.authorize(login_, password)
        print('Authorized successfully')
    except KeyError as e:
        print(e)


def register(args):
    login_ = args.login
    password = args.password
    name = args.name
    try:
        Application.register_user(name, login_, password)
        print('Registered successfully')
    except KeyError as e:
        print(e)


def print_all_users(args=None):
    for user in Application.users:
        print(Application.users[user])


def print_user(args=None):
    print(Application.cur_user)


def add_task(args):
    name = args.name
    tags = args.tags
    description = args.description
    parent_id = args.parent
    try:
        Application.add_task(name, description, tags, parent_id)
        print('Added successfully')
    except Exception as e:
        print(e)


def complete_task(args):
    id = args.id
    try:
        Application.complete_task(id)
        print('Completed successfully')
    except KeyError as e:
        print('No such id')
    except AttributeError as e:
        pass


def remove_task(args):
    task_id = args.id
    Application.cur_user.remove_task(task_id)


def move_task(args):
    source = args.source
    dest = args.destination
    try:
        Application.move_task(source, dest)
    except KeyError as e:
        print(e)
    except RecursionError as e:
        print(e)


def add_project(args):
    name = args.name
    Application.add_project(name)


def add_project_task(args):
    project_id = args.id
    name = args.name
    tags = args.tags
    description = args.description
    parent_id = args.parent
    try:
        Application.add_project_task(name, description, tags, parent_id, project_id=project_id)
        print('Added successfully')
    except Exception as e:
        print(e)


def complete_project_task(args):
    id = args.id
    try:
        Application.complete_project_task(id)
        print('Completed successfully')
    except KeyError as e:
        print('No such id')
    except AttributeError as e:
        pass


def remove_project_task(args):
    task_id = args.id
    Application.cur_user.remove_task(task_id)


def move_project_task(args):
    source = args.source
    dest = args.destination
    try:
        Application.move_project_task(source, dest)
    except KeyError as e:
        print(e)
    except RecursionError as e:
        print(e)


def print_tasks(args):
    if args.completed:
        Application.cur_user.completed_tasks.print_list()
    else:
        Application.cur_user.pending_tasks.print_list()


def print_project_tasks(args):
    if args.completed:
        Application.project.completed_tasks.print_list()
    else:
        Application.project.pending_tasks.print_list()


def print_projects(args):
    for project in Application.get_projects():
        print(project)
        print('-'*20)


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
    add_parser.add_argument('-p', '--parent', help='ID of parent task', default=0)
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser('complete', help='Complete task #ID')
    complete_parser.add_argument('-i', '--id', help='Id of completed task', required=True)
    complete_parser.set_defaults(func=complete_task)

    remove_parser = subparsers.add_parser('remove', help='Remove task #ID')
    remove_parser.add_argument('-i', '--id', help='Id of task to remove', required=True)
    remove_parser.set_defaults(func=remove_task)

    move_parser = subparsers.add_parser('move', help='Move task #source to sub tasks of task #destination')
    move_parser.add_argument('-s', '--source', help='Id of parent task', required=True)
    move_parser.add_argument('-d', '--destination', help='Id of task you want to move', required=True)
    move_parser.set_defaults(func=move_task)

    task_list_parser = subparsers.add_parser('list', help='Print all your tasks')
    print_group = task_list_parser.add_mutually_exclusive_group()
    print_group.add_argument('-p', '--pending', action='store_true', help='Print all pending tasks')
    print_group.add_argument('-c', '--completed', action='store_true', help='Print all completed tasks')
    task_list_parser.set_defaults(func=print_tasks)

    projects_parser = subparsers.add_parser('project', help='Manage projects')

    project_subparsers = projects_parser.add_subparsers(help='sub-command help')

    project_add_parser = project_subparsers.add_parser('create', help='Create new project')
    project_add_parser.add_argument('-n', '--name', help='Project name', default='Simple project', required=True)
    project_add_parser.set_defaults(func=add_project)

    project_add_parser = project_subparsers.add_parser('add', help='Add task to project task list')
    project_add_parser.add_argument('-i', '--id', help='Project id', default=0)
    project_add_parser.add_argument('-n', '--name', help='Task name', default='Simple task', required=True)
    project_add_parser.add_argument('-d', '--description', help='Task description', default='', required=False)
    project_add_parser.add_argument('-t', '--tags', help='Task tags', nargs='+', required=False)
    project_add_parser.add_argument('-p', '--parent', help='ID of parent task', default=0)
    project_add_parser.set_defaults(func=add_project_task)

    project_complete_parser = project_subparsers.add_parser('complete', help='Complete project task #ID')
    project_complete_parser.add_argument('-i', '--id', help='Id of completed task', required=True)
    project_complete_parser.set_defaults(func=complete_project_task)

    project_remove_parser = project_subparsers.add_parser('remove', help='Remove task #ID from project')
    project_remove_parser.add_argument('-i', '--id', help='Id of task to remove', required=True)
    project_remove_parser.set_defaults(func=remove_project_task)

    project_move_parser = project_subparsers.add_parser(
        'move',
        help='Move project task #source to sub tasks of task #destination'
    )
    project_move_parser.add_argument('-s', '--source', help='Id of parent task', required=True)
    project_move_parser.add_argument('-d', '--destination', help='Id of task you want to move', required=True)
    project_move_parser.set_defaults(func=move_project_task)

    project_task_list_parser = project_subparsers.add_parser('list_tasks', help='Print tasks in project #id')
    project_print_group = project_task_list_parser.add_mutually_exclusive_group()
    project_print_group.add_argument('-p', '--pending', action='store_true', help='Print all pending tasks')
    project_print_group.add_argument('-c', '--completed', action='store_true', help='Print all completed tasks')
    project_task_list_parser.set_defaults(func=print_project_tasks)

    project_list_parser = project_subparsers.add_parser('list', help='Print all projects')
    project_list_parser.set_defaults(func=print_projects)

    args = parser.parse_args()
    args.func(args)


def main():
    Application.run()
    parse_args()
    Application.save_users()
    Application.save_project()


if __name__ == '__main__':
    main()
