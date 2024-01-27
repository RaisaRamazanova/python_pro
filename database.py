import sqlite3
from sqlite3 import Error, Connection
import random
import handlers
from globals import path_questions, path_answers
from sql_data import *


def create_connection(path) -> Connection | None:
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_tables(path_questions, path_answers):
    create_questions_table = """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER,
        question TEXT,
        explanation TEXT,
        explanation_code TEXT
        );
    """
    questions_connection = create_connection(path_questions)
    execute_query(questions_connection, create_questions_table)

    create_answers_table = """
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER,
            answer TEXT,
            isRight BOOL
            );
        """
    answers_connection = create_connection(path_answers)
    execute_query(answers_connection, create_answers_table)


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


# def add_questions():
#     levels = ['junior', 'middle', 'senior']
#     for level in levels:
#         create_tables(path_questions.format(level=level), path_answers.format(level=level))
#         for i in range(4):
#             sql = "INSERT INTO questions (id, question, explanation, explanation_code) VALUES (?, ?, ?, ?)"
#             val = [(i, questions[i], explanations[i], explanation_code[i]),]
#             questions_connection = create_connection(path_questions.format(level=level))
#             execute_query_with_param(questions_connection, sql, val)
#
#             for j in range(4):
#                 sql = "INSERT INTO answers (id, answer, isRight) VALUES (?, ?, ?)"
#                 val = [(i, answers[i][j], True if j == 0 else False), ]
#                 answers_connection = create_connection(path_answers.format(level=level))
#                 execute_query_with_param(answers_connection, sql, val)


def add_questions():
    data = {
        'junior': {
            'questions': junior_questions,
            'explanations': junior_explanations,
            'explanation_code': junior_explanation_code,
            'answers': junior_answers
        },
        'middle': {
            'questions': middle_questions,
            'explanations': middle_explanations,
            'explanation_code': middle_explanation_code,
            'answers': middle_answers
        },
        'senior': {
            'questions': senior_questions,
            'explanations': senior_explanations,
            'explanation_code': senior_explanation_code,
            'answers': senior_answers
        }
    }

    for level, content in data.items():
        create_tables(path_questions.format(level=level), path_answers.format(level=level))
        for i in range(4):
            sql = "INSERT INTO questions (id, question, explanation, explanation_code) VALUES (?, ?, ?, ?)"
            val = [(i, content['questions'][i], content['explanations'][i], content['explanation_code'][i]),]
            questions_connection = create_connection(path_questions.format(level=level))
            execute_query_with_param(questions_connection, sql, val)

            for j in range(4):
                sql = "INSERT INTO answers (id, answer, isRight) VALUES (?, ?, ?)"
                val = [(i, content['answers'][i][j], True if j == 0 else False), ]
                answers_connection = create_connection(path_answers.format(level=level))
                execute_query_with_param(answers_connection, sql, val)


async def get_question_from_data(update, context, question_id, level):
    questions_connection = create_connection(path_questions.format(level=level))

    id = question_id
    cursor = questions_connection.cursor()
    cursor.execute('SELECT id, question, explanation, explanation_code FROM questions WHERE id = ?', (id,))
    question = cursor.fetchall()
    questions_connection.commit()

    answers_connection = create_connection(path_answers.format(level=level))

    cursor = answers_connection.cursor()
    cursor.execute('SELECT id, answer, isRight FROM answers WHERE id = ?', (id,))
    answers = cursor.fetchall()
    answers_connection.commit()

    list_of_answers = []
    for a in answers:
        list_of_answers.append((a[1], a[2]))
    random.shuffle(list_of_answers)

    await handlers.show_question(question[0][1], question[0][2], question[0][3], list_of_answers, update, context)
