import sys
from mysql.connector import connect, Error

TABLE_NAME = "Person"
HOST = "localhost"
USER = "root"
PASS = "password"
DATABASE = "myDB"


def getConnection():
    return connect(
        host=HOST,
        user=USER,
        password=PASS,
        # database=DATABASE
        )


def createTable():
    # 1. Создание таблицы с полями представляющими ФИО, дату рождения, пол. '
    with getConnection() as connection:
        create_db_query = f"""
        DROP DATABASE IF EXISTS MyDB;
        CREATE DATABASE MyDB;
        USE MyDB;
        CREATE TABLE {TABLE_NAME} (
                                id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(50) NOT NULL,
                                year DATE NOT NULL,
                                gender CHAR(1) NOT NULL
                                );"""    
        try:
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при создании таблицы {TABLE_NAME}: {err}")

    print(f'Таблица {TABLE_NAME} создана успешно.')


def insertRecord(name, year, gender):
    # 2. Создание записи. 
    insert_db_query = f"""INSERT INTO {TABLE_NAME} (name, year, gender) VALUES (
                                        "{name}",
                                        "{year}",
                                        "{gender}"
                                        );"""
    with getConnection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_db_query)
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Ошибка MySQL при добавлении записи в таблице {TABLE_NAME}: {err}")
    
    print('Запись создана.')


def selectRecords():
    # 3. Вывод всех строк с уникальным значением ФИО+дата, отсортированным по ФИО , вывести ФИО, Дату рождения, пол, кол-во полных лет.
    select_db_query = f"""
    /* Имя, ДwР, пол, кол-во полных лет (внешняя таблица) */
    SELECT Person.name, Person.dob, DATE_FORMAT(FROM_DAYS(DATEDIFF(now(),Person.dob)), '%Y')+0 AS age, Person.gender
    FROM Person 
    INNER JOIN
    (
        SELECT DISTINCT name, dob 
        FROM Person
    )dt
    ON Person.name = dt.name and Person.dob = dt.dob
    ORDER BY Person.name
    """

    with getConnection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(select_db_query)
                result = cursor.fetchall()
                for row in result:
                    print(row)
        except mysql.connector.Error as err:
            print(f"Ошибка MySQL при выводе записей из таблицы {TABLE_NAME}: {err}")
    
    print('Выборка завершена.')


def generateMillionRandomRecords():
    surnames = ['ivanov', 'petrov', 'sidorov', 'bochkarev', 'grachev']
    names = ['vasya', 'petya', 'masha', 'dasha', 'ivan']

    # name =  names[random index (0:len(names)-1)] + " " + surnames[random index (0:len(surnames)-1)]

    # dob = YYYY  random(1900:2022) + MM random (1:12) + DD random (1-28)
    # gender = random (0:1) M / F

    # DO 1000000 cycles

    fSurnames = ['faronov', 'farisov', 'fedorov']
    # Additionally 100 records of men with F 

# Основная программа
argv = sys.argv[1:]

len = len(argv)
if len == 0 or len > 4:
    print ('Неправильный формат параметров')
    quit()

param1 = argv[0]
if param1 == "1":
    createTable()
elif param1 == "2":
    # 2. Создание записи. Использовать следующий формат: >myApp 2 ФИО ДатаРождения Пол
    if len != 4:
        print ('Неправильный формат параметров')
        quit()
    
    your_name = argv[1]
    year_born = argv[2]
    your_sex = argv[3]

    insertRecord(your_name, year_born, your_sex)

elif param1 == "3":
    # 3. Вывод всех строк с уникальным значением ФИО+дата, отсортированным по ФИО , вывести ФИО, Дату рождения, пол, кол-во полных лет.
    # TODO
    print('---')
    
elif param1 == "4":
    # Заполнение автоматически 100 строк в которых пол мужской и ФИО начинается с "F".

    print('Добавлено в таблицу БД 100 строк, где пол мужской и поле ФИО начинается с F')

elif param1 == "5":
    # 5.  Результат выборки из таблицы по критерию: пол мужской, ФИО  начинается с "F". Сделать замер времени выполнения.
    print('Все мужчины, у которых фамилия начинается с F')

