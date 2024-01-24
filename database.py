import sqlite3
from sqlite3 import Error, Connection
import random
import handlers
from globals import path_answers, path_questions


good_stickers_id_list = [
    'CAACAgQAAxkBAAELPQplr97hg1Vh-X3xA8QKol4RDeyXXgACmAADX8YBGTYbvHBxeGbVNAQ',
    'CAACAgIAAxkBAAELPQxlr97mwC9vZScrg0p-Vcl0aT_eIQACagADpsrIDGtK7sZiKAktNAQ',
    'CAACAgEAAxkBAAELPQ5lr98puHM97K1HD-hHsnWSEfHAsAAC-wkAAr-MkAQMJ3Ulkwaw7jQE',
    'CAACAgIAAxkBAAELPRBlr9816KcFqgwiY7ESp2AQuEfHsgACHQADwDZPE17YptxBPd5INAQ'
]

bad_stickers_id_list = [
    'CAACAgIAAxkBAAELPRhlr-AMOcKdDnUX5NnrEdNyEKhDHgACYDgAAl_ywEtZdJgec6_qAzQE',
    'CAACAgIAAxkBAAELPRZlr-AJdqdAbi-HVJfiyOwLcJGSLgAC7D0AAnhtwUsfenJqLGhyATQE',
    'CAACAgIAAxkBAAELPRRlr9_-TjS7izaUVecx7Clgx75FDwACIwEAAiov8QuVnf8dwZorKTQE',
    'CAACAgIAAxkBAAELPRJlr9_6JDzof7-axb_q02h7FdVx2wACKwUAAiMFDQABW3KWmdNyE8o0BA'
]

questions = [
    'Какой символ используется для обозначения __начала комментария__ в однострочном комментарии в Python?',
    'Какой из следующих вариантов правильно определяет __пустой список__ в Python?',
    'Какой оператор используется для проверки, __принадлежит ли элемент словарю__ в Python?',
    'Какой метод используется для __добавления элемента в конец списка__ в Python?'
]

explanations = [
    'В Python символ \# используется для обозначения начала комментария в одной строке\.\nВсе\, что идет после символа \# на этой строке\, считается комментарием и игнорируется интерпретатором Python\.',
    'В Python пустой список определяется с помощью квадратных скобок \[\]\.\nЭто создает новый список\, не содержащий ни одного элемента\.',
    'В Python оператор in используется для проверки наличия элемента в словаре \(и других контейнерах\)\.\nНапример\, key in my\_dict вернет True\, если key существует в словаре my\_dict\.',
    'Метод append\(\) используется для добавления элемента в конец списка в Python\.\nНапример\, если у вас есть список my\_list\, то my\_list\.append\(item\) добавит item в конец этого списка\.'
]

explanation_code = [
    '<pre># Это комментарий в Python</pre>',
    '<pre>empty_list = []</pre>',
    '<pre>my_dict = {\'a\': 1, \'b\': 2, \'c\': 3}\nif \'a\' in my_dict:\n\tprint(\'Key \"a\" exists in the dictionary.\')</pre>',
    '<pre>my_list = [1, 2, 3]\nmy_list.append(4)  # Теперь my_list содержит [1, 2, 3, 4]</pre>'
]

answers = [
    ['#', '//', '--', '/*'],
    ['[]', 'list()', '{}', 'None'],
    ['in', 'exists', 'contains', 'has'],
    ['append()', 'add()', 'insert()', 'extend()']
]


def create_connection(path) -> Connection | None:
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_tables():
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


def add_questions():
    create_tables()
    for i in range(4):
        sql = "INSERT INTO questions (id, question, explanation, explanation_code) VALUES (?, ?, ?, ?)"
        val = [(i, questions[i], explanations[i], explanation_code[i]),]
        questions_connection = create_connection(path_questions)
        execute_query_with_param(questions_connection, sql, val)

        for j in range(4):
            sql = "INSERT INTO answers (id, answer, isRight) VALUES (?, ?, ?)"
            val = [(i, answers[i][j], True if j == 0 else False), ]
            answers_connection = create_connection(path_answers)
            execute_query_with_param(answers_connection, sql, val)


def update_questions():
    for i in range(4):
        sql = "INSERT INTO questions (id, question, explanation, explanation_code) VALUES (?, ?, ?, ?)"
        val = [(i, questions[i], explanations[i], explanation_code[i]), ]
        questions_connection = create_connection(path_questions)
        execute_query_with_param(questions_connection, sql, val)

        for j in range(4):
            sql = "INSERT INTO answers (id, answer, isRight) VALUES (?, ?, ?)"
            val = [(i, answers[i][j], True if j == 0 else False), ]
            answers_connection = create_connection(path_answers)
            execute_query_with_param(answers_connection, sql, val)


async def get_question(question_id: int):
    questions_connection = create_connection(path_questions)

    id = question_id
    cursor = questions_connection.cursor()
    cursor.execute('SELECT id, question, explanation, explanation_code FROM questions WHERE id = ?', (id,))
    question = cursor.fetchall()
    questions_connection.commit()

    answers_connection = create_connection(path_answers)

    cursor = answers_connection.cursor()
    cursor.execute('SELECT id, answer, isRight FROM answers WHERE id = ?', (id,))
    answers = cursor.fetchall()
    answers_connection.commit()

    list_of_answers = []
    for a in answers:
        list_of_answers.append((a[1], a[2]))
    random.shuffle(list_of_answers)

    await handlers.show_question(question[0][1], question[0][2], question[0][3], list_of_answers)
