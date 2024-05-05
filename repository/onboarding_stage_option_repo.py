import time


class OnboardingStageOptionRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def toggle_stage_option(self, user_id, chat_id, user_onboarding_id, user_onboarding_stage_id, stage_id,
                            stage_option_id):
        """Добавляет или удаляет опцию в этапе, в зависимости от её текущего состояния, и возвращает строку с описанием действия."""
        if stage_option_id is None:
            print("Ошибка: stage_option_id не может быть null.")
            return None  # Возвращаем None или обрабатываем ошибку соответствующим образом

        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Проверяем, существует ли уже такая опция
                    cursor.execute("""
                        SELECT id FROM user_onboarding_stage_option 
                        WHERE user_id = %s AND chat_id = %s AND user_onboarding_id = %s 
                        AND user_onboarding_stage_id = %s AND stage_id = %s AND stage_option_id = %s
                    """, (user_id, chat_id, user_onboarding_id, user_onboarding_stage_id, stage_id, stage_option_id))

                    if cursor.fetchone() is None:
                        # Если опция не существует, добавляем её
                        created_at = int(time.time())
                        cursor.execute("""
                            INSERT INTO user_onboarding_stage_option 
                            (user_id, chat_id, user_onboarding_id, user_onboarding_stage_id, stage_id, stage_option_id, created_at) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (user_id, chat_id, user_onboarding_id, user_onboarding_stage_id, stage_id, stage_option_id,
                              created_at))
                        connection.commit()
                        return "added"  # Возвращаем информацию о добавлении
                    else:
                        # Если опция существует, удаляем её
                        cursor.execute("""
                            DELETE FROM user_onboarding_stage_option 
                            WHERE user_id = %s AND chat_id = %s AND user_onboarding_id = %s 
                            AND user_onboarding_stage_id = %s AND stage_id = %s AND stage_option_id = %s
                        """, (
                        user_id, chat_id, user_onboarding_id, user_onboarding_stage_id, stage_id, stage_option_id))
                        connection.commit()
                        return "removed"  # Возвращаем информацию об удалении
        except Exception as error:
            print(f"Ошибка при изменении опции в этапе: {error}")
            return None  # Или можно выбросить исключение для обработки на более высоком уровне

    def has_stage_option(self, user_id, user_onboarding_id, user_onboarding_stage_id):
        """Проверяет, есть ли хотя бы одна опция на конкретном шаге онбординга у пользователя."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT EXISTS (
                        SELECT 1 FROM user_onboarding_stage_option 
                        WHERE user_id = %s 
                        AND user_onboarding_id = %s 
                        AND user_onboarding_stage_id = %s
                    )
                    """
                    cursor.execute(query, (user_id, user_onboarding_id, user_onboarding_stage_id))
                    exists = cursor.fetchone()[0]
                    return exists
        except Exception as error:
            print(f"Ошибка при проверке наличия опции на шаге: {error}")
            return False

    def check_user_has_stage_option(self, user_id, stage_option_id, user_onboarding_id):
        """Проверяет, есть ли у пользователя определенная опция этапа."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Формируем запрос к базе данных
                    query = """
                    SELECT EXISTS (
                        SELECT 1 FROM user_onboarding_stage_option
                        WHERE user_id = %s AND stage_option_id = %s AND user_onboarding_id = %s
                    )
                    """
                    # Выполняем запрос
                    cursor.execute(query, (user_id, stage_option_id, user_onboarding_id))
                    # Получаем результат запроса
                    exists = cursor.fetchone()[0]
                    return exists
        except Exception as error:
            print(f"Ошибка при проверке наличия опции этапа у пользователя: {error}")
            return False

    def get_user_selected_option_names(self, user_id, user_onboarding_id, chat_id):
        """Возвращает список названий выбранных пользователем опций для этапов, которые должны быть показаны."""
        selected_option_names = []
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    SELECT so.name
                    FROM user_onboarding_stage_option uoso
                    JOIN stage s ON uoso.stage_id = s.id
                    JOIN stage_option so ON uoso.stage_option_id = so.id
                    WHERE uoso.user_id = %s AND uoso.chat_id = %s AND uoso.user_onboarding_id = %s AND s.is_shown = TRUE AND so.is_enabled = TRUE
                    """
                    cursor.execute(query, (user_id, chat_id, user_onboarding_id))
                    # Извлечение результатов
                    for (option_name,) in cursor.fetchall():
                        selected_option_names.append(option_name)
            return selected_option_names
        except Exception as error:
            print(f"Ошибка при получении названий выбранных опций пользователя: {error}")
            return selected_option_names

