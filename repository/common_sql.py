import psycopg2
from data.config import *
from psycopg2 import DatabaseError


def create_connection():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        print("Connection to PostgreSQL DB successful")
    except DatabaseError as e:
        print(f"The error '{e}' occurred")
        return None

    return connection


def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except DatabaseError as e:
        print(f"The error '{e}' occurred")


def execute_query_with_param(connection, sql, val):
    try:
        cursor = connection.cursor()
        cursor.executemany(sql, val)
        connection.commit()
        print("Query executed successfully")
        cursor.close()
    except DatabaseError as e:
        print(f"The error '{e}' occurred")
    finally:
        connection.close()
        print("MySQL connection is closed")