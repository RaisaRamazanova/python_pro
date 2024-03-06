import time


class OnboardingRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def start_onboarding(self, user_id, chat_id):
        """Регистрирует начало онбординга пользователя."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    INSERT INTO user_onboarding (user_id, chat_id, started_at) 
                    VALUES (%s, %s, %s)
                    """
                    # Получаем текущее время в формате UNIX timestamp
                    started_at = int(time.time())
                    cursor.execute(query, (user_id, chat_id, started_at))
                    connection.commit()
                    return True
        except Exception as error:
            print(f"Ошибка при регистрации начала онбординга: {error}")
            return False

    def get_user_onboarding_id(self, user_id):
        """Возвращает ID самого нового процесса онбординга для пользователя."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT id FROM user_onboarding 
                    WHERE user_id = %s
                    ORDER BY started_at DESC
                    LIMIT 1
                    """
                    cursor.execute(query, (user_id,))
                    user_onboarding_id = cursor.fetchone()
                    if user_onboarding_id:
                        return user_onboarding_id[0]  # Возвращаем только ID, если запись найдена
                    else:
                        return None
        except Exception as error:
            print(f"Ошибка при получении ID процесса онбординга для пользователя с ID {user_id}: {error}")
            return None

    def finish_onboarding(self, user_id, chat_id):
        """Отмечает завершение онбординга пользователя."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE user_onboarding 
                    SET finished_at = %s 
                    WHERE user_id = %s AND chat_id = %s AND finished_at IS NULL
                    """
                    # Получаем текущее время в формате UNIX timestamp
                    finished_at = int(time.time())
                    cursor.execute(query, (finished_at, user_id, chat_id))
                    connection.commit()
                    return True
        except Exception as error:
            print(f"Ошибка при отметке завершения онбординга: {error}")
            return False
