from src import Task, TaskList, User, Application


def menu():
    print('Choose operation:')
    print('1. Add task')
    print('2. Change task')
    print('0. Exit')
    c = input()
    return c


def main():
    app = Application()
    while True:
        c = menu()
        if c == '0':
            break
        t = Task()
        print(t)


if __name__ == '__main__':
    main()
