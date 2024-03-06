import time


class InterviewQuestionRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_question(self, interview_id, question_id):
        """Создает вопрос в контексте интервью."""
        created_at = int(time.time())
        with self.db_connection.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO interview_question (interview_id, question_id, created_at)
                    VALUES (%s, %s, %s) RETURNING id
                """, (interview_id, question_id, created_at))
                question_entry_id = cursor.fetchone()[0]
                connection.commit()
                return question_entry_id

    def answer_question(self, interview_id, question_id, is_correct):
        """Регистрирует ответ пользователя на вопрос."""
        answered_at = int(time.time())
        with self.db_connection.get_connection() as connection:
            with connection.cursor() as cursor:
                # Определяем индекс для следующего вопроса
                cursor.execute("""
                    SELECT MAX(index) + 1 FROM interview_question
                    WHERE interview_id = %s
                """, (interview_id,))
                next_index = cursor.fetchone()[0] or 1
                # Отмечаем ответ на вопрос
                cursor.execute("""
                    INSERT INTO interview_question (interview_id, question_id, answered_at, is_correct_answer, index)
                    VALUES (%s, %s, %s, %s, %s)
                """, (interview_id, question_id, answered_at, is_correct, next_index))
                connection.commit()

    def get_correct_answer_percentage(self, interview_id):
        """Вычисляет процент правильных ответов в интервью."""
        with self.db_connection.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(id) FROM interview_question
                    WHERE interview_id = %s AND is_correct_answer = TRUE
                """, (interview_id,))
                correct_count = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(id) FROM interview_question
                    WHERE interview_id = %s
                """, (interview_id,))
                total_count = cursor.fetchone()[0]

                if total_count > 0:
                    return (correct_count / total_count) * 100
                else:
                    return 0
