class QuestionRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_questions_by_parameters(self, topic_id, level_id, is_enabled, language_id, interview_id):
        questions = []
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT q.id, q.topic_id, q.content, q.explanation, q.explanation_code, q.level_id, q.is_enabled, q.language_id 
                    FROM question AS q
                    WHERE q.topic_id = %s AND q.level_id = %s AND q.is_enabled = %s AND q.language_id = %s
                    AND NOT EXISTS (
                        SELECT 1
                        FROM interview_question AS iq
                        WHERE iq.question_id = q.id AND iq.interview_id = %s
                    )
                    """
                    cursor.execute(query, (topic_id, level_id, is_enabled, language_id, interview_id))
                    result = cursor.fetchall()
                    for row in result:
                        questions.append(row[0])

                    return questions
        except Exception as error:
            print(f"Ошибка при получении вопросов: {error}")
            return questions

    def get_question_by_question_id(self, question_id):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = (
                        "SELECT id, topic_id, content, explanation, explanation_code, level_id, is_enabled, language_id "
                        "FROM question WHERE id = %s")
                    cursor.execute(query, (question_id,))
                    result = cursor.fetchone()
                    if result:
                        return {
                            'id': result[0],
                            'topic_id': result[1],
                            'content': result[2],
                            'explanation': result[3],
                            'explanation_code': result[4],
                            'level_id': result[5],
                            'is_enabled': result[6],
                            'language_id': result[7]
                        }
                    else:
                        return None
        except Exception as error:
            print(f"Ошибка при получении вопроса по ID: {error}")
            return None
