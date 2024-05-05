import time


class OnboardingStageRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def start_onboarding_stage(self, user_id, chat_id, user_onboarding_id, stage_id):
        """Регистрирует начало определенного этапа онбординга для пользователя."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    INSERT INTO user_onboarding_stage 
                    (user_id, chat_id, user_onboarding_id, stage_id, created_at) 
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    # Получаем текущее время в формате UNIX timestamp
                    created_at = int(time.time())
                    cursor.execute(query, (user_id, chat_id, user_onboarding_id, stage_id, created_at))
                    connection.commit()
                    return True
        except Exception as error:
            print(f"Ошибка при регистрации начала этапа онбординга: {error}")
            return False

    def start_next_onboarding_stage(self, user_id, chat_id, user_onboarding_id):
        """Добавляет следующий шаг онбординга, если текущий шаг не является последним."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Получаем текущий шаг онбординга и его индекс
                    cursor.execute("""
                        SELECT s.id, s.index FROM stage s
                        JOIN user_onboarding_stage uos ON s.id = uos.stage_id
                        WHERE uos.user_id = %s AND uos.chat_id = %s AND uos.user_onboarding_id = %s
                        ORDER BY uos.created_at DESC LIMIT 1
                    """, (user_id, chat_id, user_onboarding_id))
                    current_stage = cursor.fetchone()

                    if current_stage is None:
                        # Если шагов нет, начинаем с первого шага, который имеет минимальный индекс
                        cursor.execute("SELECT id FROM stage WHERE is_enabled = TRUE ORDER BY index ASC LIMIT 1")
                    else:
                        current_stage_id, current_index = current_stage
                        # Проверяем, есть ли следующий шаг
                        cursor.execute("""
                            SELECT id FROM stage 
                            WHERE is_enabled = TRUE AND index > %s 
                            ORDER BY index ASC LIMIT 1
                        """, (current_index,))

                    next_stage = cursor.fetchone()
                    if next_stage is not None:
                        next_stage_id = next_stage[0]
                        created_at = int(time.time())  # Текущее время в формате UNIX timestamp
                        # Добавляем следующий шаг онбординга
                        cursor.execute("""
                            INSERT INTO user_onboarding_stage (user_id, chat_id, user_onboarding_id, stage_id, created_at) 
                            VALUES (%s, %s, %s, %s, %s)
                        """, (user_id, chat_id, user_onboarding_id, next_stage_id, created_at))
                        connection.commit()
                        return True
                    else:
                        # Если следующего шага нет, значит текущий шаг был последним
                        return False
        except Exception as error:
            print(f"Ошибка при добавлении следующего шага онбординга: {error}")
            return False

    def get_latest_onboarding_stage_details(self, user_id):
        """Получает детали самого последнего шага самого последнего (по времени начала) незавершенного онбординга."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Шаг 1: Находим ID последнего незавершенного онбординга
                    cursor.execute("""
                    SELECT id FROM user_onboarding
                    WHERE finished_at IS NULL AND user_id = %s
                    ORDER BY started_at DESC LIMIT 1
                    """, (user_id,))
                    latest_onboarding = cursor.fetchone()
                    if latest_onboarding is None:
                        return None  # Нет незавершенных онбордингов

                    user_onboarding_id = latest_onboarding[0]

                    # Шаг 2: Находим последний шаг для этого онбординга
                    cursor.execute("""
                    SELECT stage_id FROM user_onboarding_stage
                    WHERE user_onboarding_id = %s
                    ORDER BY created_at DESC LIMIT 1
                    """, (user_onboarding_id,))
                    latest_stage_id_record = cursor.fetchone()
                    if not latest_stage_id_record:
                        return None  # Онбординг есть, но шаги не начаты

                    stage_id = latest_stage_id_record[0]

                    # Шаг 3: Получаем информацию о самом последнем шаге
                    cursor.execute("""
                    SELECT name, index, is_required, description, is_enabled FROM stage
                    WHERE id = %s
                    """, (stage_id,))
                    stage_details = cursor.fetchone()

                    if stage_details:
                        return {
                            'id': stage_id,
                            "name": stage_details[0],
                            "index": stage_details[1],
                            "is_required": stage_details[2],
                            "description": stage_details[3],
                            "is_enabled": stage_details[4]
                        }
                    else:
                        return None
        except Exception as error:
            print(f"Ошибка при получении деталей последнего шага онбординга: {error}")
            return None

    def get_latest_onboarding_stage_id(self, user_id, user_onboarding_id):
        """Возвращает ID самого последнего этапа онбординга для заданного пользователя и процесса онбординга."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT id FROM user_onboarding_stage
                    WHERE user_id = %s AND user_onboarding_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """
                    cursor.execute(query, (user_id, user_onboarding_id))
                    result = cursor.fetchone()
                    if result:
                        return result[0]  # Возвращаем ID последнего этапа онбординга
                    else:
                        return None  # Если записей нет, возвращаем None
        except Exception as error:
            print(f"Ошибка при получении ID последнего этапа онбординга: {error}")
            return None

    def return_to_previous_onboarding_step(self, user_id, user_onboarding_id):
        try:
            # Устанавливаем соединение с базой данных
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Находим ID текущего шага пользователя
                    cursor.execute("""
                            SELECT stage_id FROM user_onboarding_stage
                            WHERE user_id = %s AND user_onboarding_id = %s
                            ORDER BY created_at DESC LIMIT 1
                        """, (user_id, user_onboarding_id))
                    current_stage = cursor.fetchone()
                    if current_stage:
                        current_stage_id = current_stage[0]

                        # Удаляем записи о текущем шаге из user_onboarding_stage_option
                        cursor.execute("""
                                DELETE FROM user_onboarding_stage_option
                                WHERE user_id = %s AND user_onboarding_id = %s AND stage_id = %s
                            """, (user_id, user_onboarding_id, current_stage_id))

                        # Удаляем запись о текущем шаге из user_onboarding_stage
                        cursor.execute("""
                                DELETE FROM user_onboarding_stage
                                WHERE user_id = %s AND user_onboarding_id = %s AND stage_id = %s
                            """, (user_id, user_onboarding_id, current_stage_id))

                        # Подтверждаем изменения
                        connection.commit()
                    else:
                        print("Нет текущего шага для пользователя.")
        except Exception as error:
            print(f"Ошибка при возвращении к предыдущему шагу онбординга: {error}")
