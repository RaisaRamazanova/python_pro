class InterviewTopicRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_topic(self, interview_id, topic_id):
        """Добавляет тему к интервью."""
        with self.db_connection.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO interview_topic (interview_id, topic_id)
                    VALUES (%s, %s) RETURNING id
                """, (interview_id, topic_id))
                interview_topic_id = cursor.fetchone()[0]
                connection.commit()
                return interview_topic_id

    def record_interview_topics(self, interview_id, user_onboarding_id):
        """Записывает темы интервью на основе выбранных опций в процессе онбординга."""
        try:
            # Получаем stage_option_id из user_onboarding_stage_option
            stage_option_ids = self._get_stage_option_ids_for_onboarding(user_onboarding_id)

            # Записываем каждый stage_option_id в interview_topic
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    for option_id in stage_option_ids:
                        query = """
                        INSERT INTO interview_topic (interview_id, topic_id)
                        VALUES (%s, %s);
                        """
                        cursor.execute(query, (interview_id, option_id))
                    connection.commit()
            return True
        except Exception as error:
            print(f"Ошибка при записи тем интервью: {error}")
            return False

    def _get_stage_option_ids_for_onboarding(self, user_onboarding_id):
        """Получает список stage_option_id для заданного user_onboarding_id."""
        stage_option_ids = []
        with self.db_connection.get_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                SELECT stage_option_id FROM user_onboarding_stage_option
                WHERE user_onboarding_id = %s;
                """
                cursor.execute(query, (user_onboarding_id,))
                for record in cursor.fetchall():
                    stage_option_ids.append(record[0])
        return stage_option_ids