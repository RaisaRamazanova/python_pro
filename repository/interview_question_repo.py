import time


class InterviewQuestionRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_question(self, interview_id, question_id):
        """Создает вопрос в контексте интервью."""
        created_at = int(time.time())
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Определяем индекс для нового вопроса
                    cursor.execute("""
                        SELECT COALESCE(MAX(index), 0) + 1 FROM interview_question
                        WHERE interview_id = %s
                    """, (interview_id,))
                    next_index = cursor.fetchone()[0]

                    # Добавляем вопрос с вычисленным индексом
                    cursor.execute("""
                        INSERT INTO interview_question (interview_id, question_id, created_at, index)
                        VALUES (%s, %s, %s, %s) RETURNING id
                    """, (interview_id, question_id, created_at, next_index))
                    question_entry_id = cursor.fetchone()[0]
                    connection.commit()
                    return question_entry_id
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    def get_last_unanswered_question(self, interview_id):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT *
                        FROM public.interview_question
                        WHERE interview_id = %s AND answered_at IS NULL
                        ORDER BY created_at DESC
                        LIMIT 1
                    """, (interview_id,))
                    question = cursor.fetchone()
                    return question[2]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def answer_question(self, interview_id, question_id, is_correct):
        """Регистрирует ответ пользователя на вопрос."""
        answered_at = int(time.time())
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Отмечаем ответ на вопрос
                    cursor.execute("""
                        UPDATE interview_question
                        SET answered_at = %s, is_correct_answer = %s
                        WHERE interview_id = %s AND question_id = %s
                    """, (answered_at, is_correct, interview_id, question_id))
                    connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_count_of_correct_answers(self, interview_id):
        """Возвращает количество правильных ответов в интервью."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) FROM interview_question
                        WHERE interview_id = %s AND is_correct_answer = TRUE
                    """, (interview_id,))
                    correct_answers_count = cursor.fetchone()[0]
                    return correct_answers_count
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    def get_correct_answer_percentage(self, interview_id):
        """Вычисляет процент правильных ответов в интервью."""
        try:
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
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    def get_number_of_question(self, interview_id):
        """Подсчитывает количество вопросов в интервью."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) FROM interview_question
                        WHERE interview_id = %s
                    """, (interview_id,))
                    number_of_question = cursor.fetchone()[0]
                    return number_of_question
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None