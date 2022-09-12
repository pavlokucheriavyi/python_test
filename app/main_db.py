import psycopg2
from config import host, user, password, db_name


def write_to_db(export_list):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS app;')
            print('[INFO] Table was deleted')

        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS app (
                id serial PRIMARY KEY,
                date varchar (20),
                price varchar (20),
                url varchar (200)
            );""")
            print('[INFO] Table was created')

        with connection.cursor() as cursor:
            command = """INSERT INTO app (date, price, url) VALUES (%s, %s, %s);"""
            cursor.executemany(command, export_list)
            print('[INFO] All data were inserted')

        connection.close()
        print('[INFO] Connection with database closed')

    except Exception as _ex:
        print('[INFO] Error with database', _ex)



