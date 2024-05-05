import time


class InterviewRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def start_interview(self, user_id, chat_id):
        """Начинает новое интервью для пользователя с записью времени начала."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    started_at = int(time.time())
                    query = """
                    INSERT INTO interview (user_id, chat_id, started_at)
                    VALUES (%s, %s, %s) RETURNING id;
                    """
                    cursor.execute(query, (user_id, chat_id, started_at))
                    interview_id = cursor.fetchone()[0]
                    connection.commit()
                    return interview_id
        except Exception as error:
            print(f"Ошибка при начале интервью: {error}")
            return None

    def finish_interview(self, interview_id):
        """Заканчивает интервью, записывая время завершения."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    finished_at = int(time.time())
                    query = """
                    UPDATE interview
                    SET finished_at = %s
                    WHERE id = %s;
                    """
                    cursor.execute(query, (finished_at, interview_id))
                    connection.commit()
                    return True
        except Exception as error:
            print(f"Ошибка при завершении интервью: {error}")
            return False

    def get_last_unfinished_interview_id(self, user_id, chat_id):
        """Получает идентификатор последнего по ID незавершенного интервью для пользователя."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT id FROM interview
                    WHERE user_id = %s AND chat_id = %s AND finished_at IS NULL
                    ORDER BY id DESC LIMIT 1;
                    """
                    cursor.execute(query, (user_id, chat_id))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except Exception as error:
            print(f"Ошибка при получении последнего незавершенного интервью: {error}")
            return None