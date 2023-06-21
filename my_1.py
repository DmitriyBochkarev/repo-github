# ===========================================
# Задание:
# Написать консольное приложение или php скрипт, который будет запускаться из консоли.
# По каждому пункту оно должно принимать  параметр командной строки и выполнять соответствующий пункт.
# По ходу задания будут примеры. Для ФИО использовать английский язык. Решать проблему с отображением русского языка в
# консоли, если возникает, не нужно.
# Приложение/скрипт должно подключаться к базе данных.
# В качестве СУБД можно использовать любую SQL СУБД или MongoDB.
# В качестве среды разработки можете использовать любой известный вам язык программирования.
# В приложении должно быть:
# 1. Создание таблицы с полями представляющими ФИО, дату рождения, пол.
# Пример запуска приложения:
# myApp 1
# Для php:
# php myApp.php 1
# Для java:
# java myApp.class 1
# или
# java myApp.jar 1
# 2. Создание записи. Использовать следующий формат:
# myApp 2 ФИО ДатаРождения Пол
# 3. Вывод всех строк с уникальным значением ФИО+дата, отсортированным по ФИО , вывести ФИО, Дату рождения, пол, кол-во полных лет.
# Пример запуска приложения:
# myApp 3
# 4. Заполнение автоматически 1000000 строк. Распределение пола в них должно быть относительно равномерным, начальной буквы ФИО также.
# Заполнение автоматически  100 строк в которых пол мужской и ФИО начинается с "F".
# Пример запуска приложения:
# myApp 4
# 5.  Результат выборки из таблицы по критерию: пол мужской, ФИО  начинается с "F". Сделать замер времени выполнения.
# Пример запуска приложения:
# myApp 5
# Вывод приложения должен содержать время.
# 6. Произвести определенные манипуляции над базой данных для ускорения запроса из пункта 5. Убедиться, что время исполнения уменьшилось.
# Объяснить смысл произведенных действий. Предоставить результаты замера до и после.
# Просьба для любых текстовых файлов использовать кодировку utf8.

import sys
import mysql
from mysql.connector import connect, Error
import random
from datetime import datetime

DATABASE_1 = "MyDB"
TABLE_NAME = 'Person'


def getConnection():
    return connect(
        host="localhost",
        user="root",
        password="password"
    )


def createDatabase():
    with getConnection() as connection:
        print(connection)
        # пункт 1 Создание таблицы с полями представляющими ФИО, дату рождения, пол.
        create_db_query1 = f"""
        DROP DATABASE IF EXISTS {DATABASE_1};
        CREATE DATABASE {DATABASE_1}"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(create_db_query1)
        except Error as err:
            print(f"Ошибка MySQL при создании базы данных {DATABASE_1}: {err}")


def createTable():
    createDatabase()
    with getConnection() as connection:
        print(connection)
        create_db_query1 = f"""CREATE TABLE {TABLE_NAME} (
                                    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(50) NOT NULL,
                                    dob date NOT NULL,
                                    gender CHAR(1) NOT NULL
                                    );"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""USE {DATABASE_1};""")
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при добавлении записи в таблице {TABLE_NAME}: {err}")
        try:
            with connection.cursor() as cursor:
                cursor.execute(create_db_query1)
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при создании таблицы {TABLE_NAME}: {err}")
        print(f'База данных {DATABASE_1} создана заново.')
        print(f'Таблица {TABLE_NAME} создана.')


def insertRecord(name, dob, gender):
    # 2. Создание записи.
    with getConnection() as connection:
        print(connection)
        insert_db_query = f"""INSERT INTO {TABLE_NAME} (name, dob, gender) VALUES (
                                        "{name}",
                                        "{dob}",
                                        "{gender}"
                                        );"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""USE {DATABASE_1};""")
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при выборе базы данных {DATABASE_1}: {err}")
        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_db_query)
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при добавлении записи в таблице {TABLE_NAME}: {err}")
        print('Запись создана.')



def selectRecords():
    # 3. Вывод всех строк с уникальным значением ФИО+дата, отсортированным по ФИО , вывести ФИО, Дату рождения, пол, кол-во полных лет.

    with getConnection() as connection:
        print(connection)
        select_db_query = f"""/* Имя, ДwР, пол, кол-во полных лет (внешняя таблица) */
                            SELECT Person.name, Person.dob, DATE_FORMAT(FROM_DAYS(DATEDIFF(now(),Person.dob)), '%Y')+0 AS age, Person.gender
                                FROM Person 
                                INNER JOIN (SELECT DISTINCT name, dob FROM Person)dt
                                ON Person.name = dt.name and Person.dob = dt.dob
                                ORDER BY Person.name
                            """
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""USE {DATABASE_1};""")
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при выборе базы данных {DATABASE_1}: {err}")
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
    gender_id = ["M", "F"]

    for i in range(1000000):
        name = surnames[random.randint(0, len(surnames) - 1)] + " " + names[random.randint(0, len(names) - 1)]
        dob = str(random.randint(1900, 2022)) + "." + str(random.randint(1, 12)) + "." + str(random.randint(1, 28))
        gender = gender_id[random.randint(0, 1)]

        with getConnection() as connection:
            print(connection)
            insert_db_query = f"""INSERT INTO {TABLE_NAME} (name, dob, gender) VALUES (
                                                    "{name}",
                                                    "{dob}",
                                                    "{gender}"
                                                    );"""
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"""USE {DATABASE_1};""")
                connection.commit()
            except Error as err:
                print(f"Ошибка MySQL при выборе базы данных {DATABASE_1}: {err}")
            try:
                with connection.cursor() as cursor:
                    cursor.execute(insert_db_query)
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Ошибка MySQL при добавлении записи в таблице {TABLE_NAME}: {err}")
            print(f'Запись {i} создана.')


def generateFRecords():
    names = ['vasya', 'petya', 'masha', 'dasha', 'ivan']
    gender_id = ["M", "F"]
    fSurnames = ['faronov', 'farisov', 'fedorov']

    for i in range(100):
        name = fSurnames[random.randint(0, len(fSurnames) - 1)] + " " + names[random.randint(0, len(names) - 1)]
        dob = str(random.randint(1900, 2022)) + "." + str(random.randint(1, 12)) + "." + str(random.randint(1, 28))
        gender = gender_id[random.randint(0, 1)]

        with getConnection() as connection:
            print(connection)
            insert_db_query = f"""INSERT INTO {TABLE_NAME} (name, dob, gender) VALUES (
                                                    "{name}",
                                                    "{dob}",
                                                    "{gender}"
                                                    );"""
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"""USE {DATABASE_1};""")
                connection.commit()
            except Error as err:
                print(f"Ошибка MySQL при выборе базы данных {DATABASE_1}: {err}")
            try:
                with connection.cursor() as cursor:
                    cursor.execute(insert_db_query)
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Ошибка MySQL при добавлении записи в таблице {TABLE_NAME}: {err}")
            print(f'Запись {i} создана.')


def selectFRecords():
    # 5. Результат выборки из таблицы по критерию: пол мужской, ФИО  начинается с "F". Сделать замер времени выполнения.

    with getConnection() as connection:
        print(connection)
        select_db_query_f = f"""SELECT * FROM {TABLE_NAME}
                                  WHERE gender='M' and name LIKE 'f%';"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""USE {DATABASE_1};""")
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при выборе базы данных {DATABASE_1}: {err}")
        start_time = datetime.now()
        try:
            with connection.cursor() as cursor:
                cursor.execute(select_db_query_f)
                result = cursor.fetchall()
                for row in result:
                    print(row)
        except mysql.connector.Error as err:
            print(f"Ошибка MySQL при выводе записей из таблицы {TABLE_NAME}: {err}")
        print(f'Выборка завершена. Время выполнения {datetime.now() - start_time}')


def createIndex():
    # 6. Создание индексов для уменьшения времени выполнения запроса.
    with getConnection() as connection:
        print(connection)
        index_db_query = f"""ALTER TABLE {TABLE_NAME}
                                ADD INDEX (name, gender);"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""USE {DATABASE_1};""")
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при выборе базы данных {DATABASE_1}: {err}")
        try:
            with connection.cursor() as cursor:
                cursor.execute(index_db_query)
            connection.commit()
        except Error as err:
            print(f"Ошибка MySQL при создании индекса в таблице {TABLE_NAME}: {err}")
        print('Индексы созданы.')


# основная программа
argv = sys.argv[1:]

length = len(argv)
if length == 0 or length > 4:
    print('Неправильный формат параметров')
    quit()

param1 = argv[0]

if param1 == "1":  # пункт 1 Создание базы данных и таблицы
    createTable()

elif param1 == "2":  # пункт 2 Создание записи

    if len != 4:
        print('Неправильный формат параметров')
        quit()

    your_name = argv[1]
    birthday = argv[2]
    your_gender = argv[3]

    insertRecord(your_name, birthday, your_gender)

elif param1 == "3":  # Пункт 3 Вывод всех строк с уникальным значением ФИО+дата, отсортированным по ФИО , вывести ФИО, Дату рождения, пол, кол-во полных лет.
    selectRecords()

    # TODO
    print('---')

elif param1 == "4":
    # 4. Заполнение автоматически 1000000 строк. Распределение пола в них должно быть относительно равномерным, начальной буквы ФИО также.
    # Заполнение автоматически  100 строк в которых пол мужской и ФИО начинается с "F".

    generateMillionRandomRecords()

    # Заполнение автоматически 100 строк в которых пол мужской и ФИО начинается с "F"

    generateFRecords()

elif param1 == "5":
    # 5.  Результат выборки из таблицы по критерию: пол мужской, ФИО  начинается с "F". Сделать замер времени выполнения.

    selectFRecords()

elif param1 == "6":
    # 6. Произвести определенные манипуляции над базой данных для ускорения запроса из пункта 5. Убедиться, что время исполнения уменьшилось.
    # Объяснить смысл произведенных действий. Предоставить результаты замера до и после.
        # Чтобы уменьшить время выполнения запроса, добавим индексы для колонок "name" и "gender".
        # Если такие таблицы не имеют индекса полей, то при запросах на выборку будут долго перебираться все строки подряд,
        # пока не будет найдено искомое значение.
    createIndex()
        # сделаем повторный замер времени выполнения запроса
    selectFRecords()



