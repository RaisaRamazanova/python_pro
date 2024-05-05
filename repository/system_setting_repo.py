class SystemSettingRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_interview_question_count(self):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = "SELECT value FROM setting WHERE key = 'interview_question_count'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    return int(result[0]) if result else None
        except Exception as error:
            print(f"Ошибка при получении количества вопросов для интервью: {error}")
            return None

    def get_theme_question_count(self):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = "SELECT value FROM setting WHERE key = 'theme_question_count'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    return int(result[0]) if result else None
        except Exception as error:
            print(f"Ошибка при получении количества вопросов для темы: {error}")
            return None
