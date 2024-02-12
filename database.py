import sqlite3
from sqlite3 import Error, Connection
import random
import test_process
from data.globals import data_path
from data.python_sql_data import *


def create_connection(path) -> Connection | None:
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_tables(path):
    create_table = """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER,
        question TEXT,
        explanation TEXT,
        explanation_code TEXT,
        answer_1 TEXT,
        answer_2 TEXT,
        answer_3 TEXT,
        answer_4 TEXT
        );
    """
    connection = create_connection(path)
    execute_query(connection, create_table)


def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query_with_param(connection, sql, val):
    try:
        cursor = connection.cursor()
        cursor.executemany(sql, val)
        connection.commit()
        print("Query executed successfully")
        cursor.close()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        connection.close()
        print("MySQL connection is closed")


def add_questions():
    data = {
        'junior': {
            'id': junior_id,
            'questions': junior_questions,
            'explanations': junior_explanations,
            'explanation_code': junior_explanation_code,
            'answers': junior_answers
        },
        'middle': {
            'id': middle_id,
            'questions': middle_questions,
            'explanations': middle_explanations,
            'explanation_code': middle_explanation_code,
            'answers': middle_answers
        },
        'senior': {
            'id': senior_id,
            'questions': senior_questions,
            'explanations': senior_explanations,
            'explanation_code': senior_explanation_code,
            'answers': senior_answers
        }
    }

    create_tables(data_path)
    for level, content in data.items():
        for i in range(len(content['id'])):
            sql = (
                "INSERT INTO questions (id, question, explanation, explanation_code, answer_1, answer_2, answer_3, "
                "answer_4) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
            val = [(
                content['id'][i], content['questions'][i], content['explanations'][i], content['explanation_code'][i],
                content['answers'][i][0], content['answers'][i][1], content['answers'][i][2], content['answers'][i][3]),]
            data_connection = create_connection(data_path)
            execute_query_with_param(data_connection, sql, val)


async def get_question_from_data(update, context, question_id):
    questions_connection = create_connection(data_path)

    # id = question_id
    id = int(str(11051)+str(question_id)[5:])
    cursor = questions_connection.cursor()
    cursor.execute('SELECT id, question, explanation, explanation_code, answer_1, answer_2, answer_3, answer_4 FROM '
                   'questions WHERE id = ?', (id,))
    data = cursor.fetchall()
    questions_connection.commit()

    last_four_elements=data[0][-4:]
    list_of_answers = [(last_four_elements[0], 1), (last_four_elements[1], 0), (last_four_elements[2], 0), (last_four_elements[3], 0)]
    random.shuffle(list_of_answers)

    await test_process.send_question_data(data[0][1], data[0][2], data[0][3], list_of_answers, question_id, update, context)