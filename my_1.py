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
# Результат прислать письмом на адрес office@ptmk.ru , в теме обязательно указать ФИО.
import sys
from mysql.connector import connect, Error
DATABASE_1 = "MyDB"
TABLE_NAME = 'Person'


def getConnection ():
    return connect(
        host="localhost",
        user="root",
        password="password"
        )

def createDatabase ():
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

argv = sys.argv[1:]

len = len(argv)
if len == 0 or len > 4:
    print ('Неправильный формат параметров')
    quit()

param1 = argv[0]
if param1 == "1":
    createDatabase()
    
    try:
        with getConnection () as connection:
            print(connection)
            tab = input("Введите название таблицы: ")
            create_db_query1 = f"""USE {DATABASE_1};
                                    CREATE TABLE {tab} (
                                        id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                        name VARCHAR(50) NOT NULL,
                                        year date NOT NULL,
                                        gender CHAR(1) NOT NULL
                                        );"""
            with connection.cursor() as cursor:
                cursor.execute(create_db_query1)
            connection.commit()

    # пункт 2 Создание записи

        while True:
            your_name = input("Введите ФИО: ")
            if your_name != "":
                year_born = input("Введите дату рождения в формате 0000-00-00: ")
                your_sex = input("Введите ваш пол (M / F): ")
                create_db_query2 = f"""INSERT INTO {tab} (name, year, gender) VALUES (
                                        "{your_name}",
                                        "{year_born}",
                                        "{your_sex}"
                                        );"""
                with connection.cursor() as cursor:
                    cursor.execute(create_db_query2)
                connection.commit()
            else:
                break

    # Пункт 3 Вывод всех строк с уникальным значением ФИО+дата, отсортированным по ФИО , вывести ФИО, Дату рождения, пол, кол-во полных лет.

        create_db_query3 = f"""SELECT DISTINCT name, year
                                FROM {tab}
                                ORDER BY name;"""
        with connection.cursor() as cursor:
            cursor.execute(create_db_query3)
            result = cursor.fetchall()
            for row in result:
                print(row)
        connection.commit()

    # вывести ФИО, Дату рождения, пол, кол-во полных лет.
        import datetime
        create_db_query3 = f"""SELECT name, year, gender
                                FROM {tab};"""
        with connection.cursor() as cursor:
            cursor.execute(create_db_query3)
            result = cursor.fetchall()
            for row in result:
                print(row)
                a = datetime.date(year=int(row[1][:4]), month=int(row[1][5:7]), day=int(row[1][8:]))
                b = datetime.date(year=2023, month=5, day=9)
                print("Количество полных лет ", int((b - a).days / (365.2425)))
        connection.commit()

    # 4. Заполнение автоматически 1000000 строк. Распределение пола в них должно быть относительно равномерным, начальной буквы ФИО также.
    # Заполнение автоматически  100 строк в которых пол мужской и ФИО начинается с "F".

        from faker import Faker
        fake = Faker()
        for i in range(1000000):
            row = fake.simple_profile()
            your_name = row.get('name')
            year_born = row.get('birthdate')
            your_sex = row.get('sex')
            create_db_query4 = f"""INSERT INTO {tab} (name, year, gender) 
                                    VALUES (
                                    "{your_name}",
                                    '{year_born}',
                                    "{your_sex}"
                                    );"""
            with connection.cursor() as cursor:
                cursor.execute(create_db_query4)
            connection.commit()

    # Заполнение автоматически  100 строк в которых пол мужской и ФИО начинается с "F"

        number = 0
        while number <= 100:
            row = fake.simple_profile()
            your_name = row.get('name')
            if your_name[0] == 'F':
                number += 1
                year_born = row.get('birthdate')
                your_sex = row.get('sex')
                create_db_query4 = f"""INSERT INTO {tab} (name, year, gender) 
                                        VALUES (
                                        "{your_name}",
                                        '{year_born}',
                                        "{your_sex}"
                                        );"""
                with connection.cursor() as cursor:
                    cursor.execute(create_db_query4)
                connection.commit()

    # 5.  Результат выборки из таблицы по критерию: пол мужской, ФИО  начинается с "F". Сделать замер времени выполнения.

        create_db_query5 = f"""SELECT * FROM {tab}
                                WHERE gender='M' and name LIKE 'F%';"""
        with connection.cursor() as cursor:
            cursor.execute(create_db_query5)
            result = cursor.fetchall()
            for row in result:
                print(row)
        connection.commit()

    # 6. Произвести определенные манипуляции над базой данных для ускорения запроса из пункта 5. Убедиться, что время исполнения уменьшилось.
    # Объяснить смысл произведенных действий. Предоставить результаты замера до и после.

        # Чтобы уменьшить время выполнения запроса, добавим индексы для колонок "name" и "gender".
        # Если такие таблицы не имеют индекса полей, то при запросах на выборку будут перебираться все строки подряд,
        # пока не будет найдено искомое значение.

        create_db_query6 = f"""ALTER TABLE {tab}
                                ADD INDEX (name, gender);"""
        with connection.cursor() as cursor:
            cursor.execute(create_db_query6)
        connection.commit()
        # результаты замера времени выполнения запроса до и после индексации представлены на скриншотах во вложении к письму

    except Error as e:
        print(e)

