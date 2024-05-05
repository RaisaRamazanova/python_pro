import time


class AnswerRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_answers_by_question_id(self, question_id):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = "SELECT id, question_id, content, is_correct FROM answer WHERE question_id = %s"
                    cursor.execute(query, (question_id,))
                    results = cursor.fetchall()
                    answers = [{'id': row[0], 'question_id': row[1], 'content': row[2], 'is_correct': row[3]} for row in results]
                    return answers
        except Exception as error:
            print(f"Ошибка при получении ответов по ID вопроса: {error}")
            return []
