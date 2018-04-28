from src import Task, TaskList, User, Application


def start_menu():
    print('Hi')
    print('1) Login')
    print('2) Register')
    c = input()
    return c


def menu():
    print('Choose operation:')
    print('1. Add task')
    print('2. Change task')
    print('0. Exit')
    c = input()
    return c


def main():
    logged_in = False
    task_list = TaskList({})
    while True:
        if not logged_in:
            c = start_menu()
            if c == '1':
                login = input('Login: ')
                password = input('Password: ')
                try:
                    Application.authorize(login, password)
                    logged_in = True
                except KeyError as e:
                    print(e)
                    continue
            elif c == '2':
                login = input('Login: ')
                password = input('Password: ')
                name = input('Name: ')
        c = menu()
        if c == '0':
            break
        t = Task()
        task_list.add_task(t)
        print(t)
    task_list.print_list()
    Application.save_task_list(task_list)


if __name__ == '__main__':
    main()
