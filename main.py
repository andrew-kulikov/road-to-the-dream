from src import Task, TaskList, User, Application
import argparse


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
        print(user)


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


def print_tasks(args):
    if args.pending:
        print(Application.cur_user.pending_tasks)
    elif args.completed:
        print(Application.cur_user.completed_tasks)


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

    task_list_parser = subparsers.add_parser('list', help='Print all your tasks')
    print_group = task_list_parser.add_mutually_exclusive_group()
    print_group.add_argument('-p', '--pending', action='store_true', help='Print all pending tasks')
    print_group.add_argument('-c', '--completed', action='store_true', help='Print all completed tasks')
    task_list_parser.set_defaults(func=print_tasks)

    args = parser.parse_args()
    args.func(args)


def main():
    Application.run()
    parse_args()
    Application.save_users()


if __name__ == '__main__':
    main()
