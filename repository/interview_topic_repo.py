class InterviewTopicRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def record_interview_topics(self, interview_id, user_onboarding_id):
        """Записывает темы интервью на основе выбранных опций в процессе онбординга."""
        try:
            topic_ids = self._get_stage_option_ids_for_onboarding(user_onboarding_id)
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    for topic_id in topic_ids:
                        query = """
                        INSERT INTO interview_topic (interview_id, topic_id)
                        VALUES (%s, %s);
                        """
                        cursor.execute(query, (interview_id, topic_id))
                    connection.commit()
            return True
        except Exception as error:
            print(f"Ошибка при записи тем интервью: {error}")
            return False

    def _get_stage_option_ids_for_onboarding(self, user_onboarding_id):
        """Получает список topic_id для изучаемых опций на основе user_onboarding_id."""
        topic_ids = []
        with self.db_connection.get_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                SELECT so.id 
                FROM user_onboarding_stage_option uoso
                JOIN stage_option so ON uoso.stage_option_id = so.id
                JOIN stage s ON so.stage_id = s.id
                WHERE uoso.user_onboarding_id = %s AND s.is_studied = TRUE;
                """
                cursor.execute(query, (user_onboarding_id,))
                for record in cursor.fetchall():
                    topic_ids.append(record[0])
        return topic_ids

    def get_topic_with_insufficient_questions(self, interview_id, user_id):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Получаем уровни пользователя
                    cursor.execute("SELECT level_id FROM user_level WHERE user_id = %s", (user_id,))
                    user_levels = [level[0] for level in cursor.fetchall()]

                    # Если у пользователя нет уровней, возвращаем None
                    if not user_levels:
                        return None

                    # Получаем темы, связанные с интервью
                    cursor.execute("SELECT topic_id FROM interview_topic WHERE interview_id = %s", (interview_id,))
                    interview_topics = [topic[0] for topic in cursor.fetchall()]

                    # Для каждой темы и каждого уровня пользователя проверяем количество вопросов
                    for topic_id in interview_topics:
                        for level_id in user_levels:
                            query = """
                            SELECT COUNT(*)
                            FROM interview_question iq
                            JOIN question q ON iq.question_id = q.id
                            WHERE iq.interview_id = %s AND q.topic_id = %s AND q.level_id = %s
                            """
                            cursor.execute(query, (interview_id, topic_id, level_id))
                            question_count = cursor.fetchone()[0]

                            if question_count < 2:
                                return topic_id, level_id
        except Exception as error:
            print(f"Ошибка при получении темы с недостаточным количеством вопросов: {error}")
        return None, None

