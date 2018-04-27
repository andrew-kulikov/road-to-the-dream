from src import Task, TaskList, User, Application


def menu():
    print('Choose operation:')
    print('1. Add task')
    print('2. Change task')
    print('0. Exit')
    c = input()
    return c


def main():
    Application.save_users()
    task_list = TaskList({})
    while True:
        c = menu()
        if c == '0':
            break
        t = Task()
        task_list.add_task(t)
        print(t)
    task_list.print_list()


if __name__ == '__main__':
    main()
