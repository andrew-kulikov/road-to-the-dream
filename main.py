from src import Task, TaskList, User, Application
import argparse


def login():
    pass


def parse_args():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-command help')
    login_parser = subparsers.add_parser('login', help='Log in as user *login*')
    login_parser.add_argument('--login', help='Your login', default='vasya')

    args = parser.parse_args()


def main():
    #Application.run()
    #Application.register_user('vasya', 'vasya', '123')
    #Application.save_users()
    print('kek')
    logged_in = False
    task_list = TaskList({})


if __name__ == '__main__':
    main()
