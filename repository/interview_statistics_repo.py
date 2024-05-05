class InterviewStatisticsRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_all_correct_answers_percentages(self):
        """Получает все значения процентов правильных ответов."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT percentage_of_correct_answers FROM public.interview_statistics")
                    percentages = [row[0] for row in cursor.fetchall()]
                    return percentages
        except Exception as e:
            print(f"Ошибка при получении процентов правильных ответов: {e}")
            return []

    def get_all_travel_times(self):
        """Получает все значения времени прохождения."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT travel_time FROM public.interview_statistics")
                    travel_times = [row[0] for row in cursor.fetchall()]
                    return travel_times
        except Exception as e:
            print(f"Ошибка при получении времен прохождения: {e}")
            return []

    def calculate_travel_time(self, interview_id):
        """Вычисляет время, затраченное на интервью."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT finished_at - started_at FROM public.interview
                        WHERE id = %s
                    """, (interview_id,))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except Exception as e:
            print(f"Ошибка при вычислении времени интервью: {e}")
            return None

    def calculate_percentage_of_correct_answers(self, interview_id):
        """Вычисляет процент правильных ответов."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) FROM public.interview_question
                        WHERE interview_id = %s
                    """, (interview_id,))
                    total_questions = cursor.fetchone()[0]
                    cursor.execute("""
                        SELECT COUNT(*) FROM public.interview_question
                        WHERE interview_id = %s AND is_correct_answer = TRUE
                    """, (interview_id,))
                    correct_answers = cursor.fetchone()[0]
                    return (correct_answers / total_questions) * 100 if total_questions else 0
        except Exception as e:
            print(f"Ошибка при вычислении процента правильных ответов: {e}")
            return None

    def save_statistics(self, interview_id):
        """Записывает статистику интервью в базу данных."""
        travel_time = self.calculate_travel_time(interview_id)
        percentage_of_correct_answers = self.calculate_percentage_of_correct_answers(interview_id)

        if travel_time is not None and percentage_of_correct_answers is not None:
            try:
                with self.db_connection.get_connection() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO public.interview_statistics (interview_id, percentage_of_correct_answers, travel_time)
                            VALUES (%s, %s, %s)
                        """, (interview_id, percentage_of_correct_answers, travel_time))
                        connection.commit()
                        return True
            except Exception as e:
                print(f"Ошибка при записи статистики: {e}")
                return False
        else:
            print("Не удалось вычислить статистику для записи.")
            return False
