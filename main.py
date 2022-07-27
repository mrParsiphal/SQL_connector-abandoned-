import MySQLdb
from format_text import green, red, blue, italic


def body():
    db, cur = login()
    exit_program = False
    while exit_program == False:
        command = input('Введите комманду: ')
        if command == 'set stroke':
            set_stroke(cur, db)
        elif command == 'show tables':
            show_tables(cur)
        elif command == 'create table':
            create_table(cur)
        elif command == 'create tab':
            create_tab(cur)
        elif command == 'create db':
            create_db(cur)
        elif command == 'connect database':
            connect_database(cur)
        elif command == 'exit':
            print("Завершение работы")
            db.close()
            exit_program = True


def answer_yes(answer):
    return answer in ('yes', 'YES')


def answer_no(answer):
    return answer in ('no', 'NO')


def read_user_data():
    host = input("Введите IP-адресс базы данных: ")
    user = input("Введите логин: ")
    password = input("Введите пароль: ")
    return host, user, password


def login():
    print((italic("Подключение к базе данных:")))
    not_repeate = False
    t = False
    while (t == False):
        config = open('config.txt', 'r')
        if config.read(1) != '':
            answer = input("Использовать данные предыдущего входа? (YES/NO): ")
            if answer_yes(answer):
                data = (config.readlines())
                host = data[0][6:-1]
                user = data[1][7:-1]
                password = data[2][11:]
                not_repeate = True
                t = 1
            elif answer_no(answer):
                host, user, password = read_user_data()
                t = True
        else:
            host, user, password = read_user_data()
            t = True
            config.close()
    login_successfully = False
    while login_successfully == False:
        try:
            print('host =', green(host))
            print('user =', green(user))
            print('password =', green('*' * len(password)))
            db = MySQLdb.connect(
                host=host,
                user=user,
                password=password,
                database='')
            print(italic('connection success'))
            cur = db.cursor()
            login_successfully = True
        except Exception as error:
            print(red(error))
            print(italic('connection failure'), end='\n\n')
            host, user, password = read_user_data()
    if not_repeate == False:
        answer = input("Сохранить данные пользователя? (YES/NO): ")
        if answer_yes(answer):
            config = open('config.txt', 'w+')
            config.write(f'''host = {host}\nuser = {user}\npassword = {password}''')
    return db, cur


def connect_database(cur):
    cur.execute('''SHOW DATABASES''')
    print(cur.fetchall())
    database = input("Введите название базы данных: ")
    try:
        cur.execute(f'''USE {database}''')
        print(italic(f"База данных {database} подключена"))
    except:
        print(italic("Не удалось подключится"))


def show_tables(cur):
    try:
        cur.execute('''SHOW TABLES''')
        print(cur.fetchall())
    except Exception as error:
        print(red(error))


def create_table(cur):
    name = input("Укажите имя таблицы: ")
    t = False
    while t == False:
        quantity_column = input("Укажите количество столбцов: ")
        if quantity_column.isdigit():
            t = True
        else:
            print("Укажите число!")

    try:
        cur.execute(f'''
        CREATE TABLE {name}
        (
        id serial PRIMARY KEY NOT NULL
        )''')
    except Exception as error:
        print(red(error))



def set_stroke(cur, db):
    nam = input("Введите 'name': ")
    age = input("Введите 'ages': ")
    lik = input("Введите 'likes': ")
    if nam.isalpha():
        if len(nam) <= 20:
            if age.isdigit():
                if len(lik) <= 100:
                    # try:
                    command = ("INSERT INTO human (name, ages, likes) VALUE (%s, %s, %s)")
                    data = (nam, age, lik)
                    cur.execute(command, data)
                    db.commit()
                    print("success!")
                # except:
                #     print("херня переделывай!")
                else:
                    print("'likes' не должно превышать 100 символов!")
            else:
                print("'ages' должно состоять из цифр!")
        else:
            print("'name' не должно превышать 20-ти символов!")
    else:
        print("'name' должно стостоять из букв!")


def create_tab(cur):
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS human 
                    (
                    id serial PRIMARY KEY NOT NULL,
                    name varchar(20) NOT NULL,
                    ages int NOT NULL,
                    likes varchar(100) NOT NULL
                    );''')
        print('success')
    except ValueError:
        print('CREATE failure')


def create_db(cur):
    db_name = input("Введите название базы данных:")
    try:
        cur.execute(f'''CREATE DATABASE {db_name}''')
        print("success")
    except ValueError:
        print("failure")


if __name__ == '__main__':
    body()
