import time


class InterviewQuestionAnswerRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_answer(self, interview_id, interview_question_id, interview_topic_id, topic_id, question_id, answer_id):
        created_at = int(time.time())
        cursor = self.db_connection.cursor()
        query = """
        INSERT INTO interview_question_answers (
            interview_id, interview_question_id, interview_topic_id, 
            topic_id, question_id, answer_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            interview_id, interview_question_id, interview_topic_id,
            topic_id, question_id, answer_id, created_at
        )
        cursor.execute(query, params)
        self.db_connection.commit()
        answer_id = cursor.lastrowid
        cursor.close()
        return answer_id
