class UserLevelRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_levels_by_user_id(self, user_id):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = "SELECT level_id FROM user_level WHERE user_id = %s"
                    cursor.execute(query, (user_id,))
                    return [level[0] for level in cursor.fetchall()]
        except Exception as error:
            print(f"Ошибка при получении уровней пользователя: {error}")
            return []

    def _get_selected_levels_for_stage(self, user_id, stage_id):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Сначала находим последний процесс онбординга
                    cursor.execute("""
                    SELECT MAX(user_onboarding_id)
                    FROM user_onboarding_stage_option
                    WHERE user_id = %s
                    """, (user_id,))
                    last_onboarding_id = cursor.fetchone()[0]

                    if last_onboarding_id is None:
                        return []  # Нет процессов онбординга для этого пользователя

                    # Теперь находим уровни для этого процесса онбординга
                    cursor.execute("""
                    SELECT stage_option_id
                    FROM user_onboarding_stage_option
                    WHERE user_id = %s AND stage_id = %s AND user_onboarding_id = %s
                    """, (user_id, stage_id, last_onboarding_id))
                    return [item[0] for item in cursor.fetchall()]
        except Exception as error:
            print(f"Ошибка при получении выбранных уровней: {error}")
            return []

    def _map_stage_options_to_levels(self, stage_option_ids):
        if not stage_option_ids:
            return []

        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = f"SELECT id FROM level WHERE stage_option_id IN %s"
                    cursor.execute(query, (tuple(stage_option_ids),))
                    return [item[0] for item in cursor.fetchall()]
        except Exception as error:
            print(f"Ошибка при сопоставлении опций этапа с уровнями: {error}")
            return []

    def _add_user_levels(self, user_id, level_ids):
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Удалить существующие уровни перед вставкой новых
                    delete_query = "DELETE FROM user_level WHERE user_id = %s"
                    cursor.execute(delete_query, (user_id,))

                    # Вставить новые уровни
                    insert_query = "INSERT INTO user_level (user_id, level_id) VALUES (%s, %s)"
                    for level_id in level_ids:
                        cursor.execute(insert_query, (user_id, level_id))
                    connection.commit()
        except Exception as error:
            print(f"Ошибка при добавлении уровней пользователя: {error}")
            connection.rollback()

    # Метод, который объединяет всё вместе
    def record_user_levels(self, user_id):
        stage_option_ids = self._get_selected_levels_for_stage(user_id, 6)
        level_ids = self._map_stage_options_to_levels(stage_option_ids)
        self._add_user_levels(user_id, level_ids)
