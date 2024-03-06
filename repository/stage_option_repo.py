class StageOptionRepository:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_stage_option_by_id(self, option_id):
        """Возвращает детали опции этапа по её ID в виде словаря."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Определение и выполнение SQL-запроса
                    query = "SELECT id, stage_id, name, is_enabled, topic_id FROM stage_option WHERE id = %s"
                    cursor.execute(query, (option_id,))
                    stage_option = cursor.fetchone()

                    # Проверка наличия результата запроса
                    if stage_option:
                        # Преобразование результата в словарь
                        option_details = {
                            "id": stage_option[0],
                            "stage_id": stage_option[1],
                            "name": stage_option[2],
                            "is_enabled": bool(stage_option[3]),  # Преобразование в bool для ясности
                            "topic_id": stage_option[4]
                        }
                        return option_details
                    else:
                        return None
        except Exception as error:
            print(f"Ошибка при получении деталей опции этапа по ID {option_id}: {error}")
            return None

    def get_stage_option_by_stage_id(self, stage_id):
        """Возвращает все опции этапа по его ID в виде списка словарей."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "SELECT id, stage_id, name, is_enabled, topic_id FROM stage_option WHERE stage_id = %s AND is_enabled = TRUE"
            cursor.execute(query, (stage_id,))
            options = cursor.fetchall()  # Извлекаем все строки, соответствующие stage_id
            cursor.close()
            # Преобразуем результаты в список словарей
            options_list = [
                {"id": option[0], "stage_id": option[1], "name": option[2], "is_enabled": option[3],
                 "topic_id": option[4]}
                for option in options
            ]
            return options_list
        except Exception as error:
            print(f"Ошибка при получении опций этапа по ID {stage_id}: {error}")
            return []

    def get_child_options_by_option_id(self, option_id):
        """Возвращает детали всех дочерних опций для заданной опции."""
        try:
            # Подключение к базе данных и создание курсора
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()

            # Получение всех child_option_id для заданного parent_option_id
            cursor.execute("""
                SELECT child_option_id 
                FROM stage_option_dependency 
                WHERE parent_option_id = %s
            """, (option_id,))
            child_option_ids = cursor.fetchall()

            # Если дочерние опции существуют, получаем их детали
            if child_option_ids:
                child_option_ids = [id[0] for id in child_option_ids]  # Преобразуем список кортежей в список ID
                query_placeholders = ', '.join(['%s'] * len(child_option_ids))  # Создаем плейсхолдеры для SQL запроса
                cursor.execute(f"""
                    SELECT * 
                    FROM stage_option 
                    WHERE id IN ({query_placeholders})
                """, tuple(child_option_ids))
                child_options = cursor.fetchall()  # Получаем детали всех дочерних опций
                return child_options
            else:
                return []  # Возвращаем пустой список, если дочерние опции отсутствуют
        except Exception as error:
            print(f"Ошибка при получении дочерних опций: {error}")
            return None

    def get_stage_option_id_by_name(self, option_name, stage_id=None):
        """Возвращает ID опции этапа по её названию (и, опционально, по ID этапа)."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            if stage_id:
                query = "SELECT id FROM stage_option WHERE name = %s AND stage_id = %s"
                cursor.execute(query, (option_name, stage_id))
            else:
                query = "SELECT id FROM stage_option WHERE name = %s"
                cursor.execute(query, (option_name,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]  # Возвращаем ID опции этапа
            else:
                return None  # Опция с таким названием не найдена
        except Exception as error:
            print(f"Ошибка при получении ID опции этапа по названию {option_name}: {error}")
            return None

    def get_next_stage_options(self, user_id, user_onboarding_id, current_stage_id):
        """Возвращает stage_option для следующего шага на основе выбранных опций текущего stage и индекса следующего stage."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Определяем индекс текущего stage
                    cursor.execute("""
                        SELECT index FROM stage
                        WHERE id = %s
                    """, (current_stage_id,))
                    current_stage_index = cursor.fetchone()[0]

                    # Находим следующий stage по индексу
                    cursor.execute("""
                        SELECT id FROM stage
                        WHERE index = %s + 1 AND is_enabled = TRUE
                    """, (current_stage_index,))
                    next_stage = cursor.fetchone()
                    if not next_stage:
                        # Если следующего stage нет, возвращаем пустой список
                        return []

                    next_stage_id = next_stage[0]

                    # Получаем stage_option_id выбранных опций текущего stage
                    cursor.execute("""
                        SELECT stage_option_id FROM user_onboarding_stage_option
                        WHERE user_id = %s AND user_onboarding_id = %s AND stage_id = %s
                    """, (user_id, user_onboarding_id, current_stage_id))
                    selected_option_ids = [option_id[0] for option_id in cursor.fetchall()]

                    if not selected_option_ids:
                        return []

                    # Находим доступные опции для следующего stage, которые являются дочерними для выбранных опций
                    selected_option_ids_placeholder = ', '.join(['%s'] * len(selected_option_ids))
                    cursor.execute(f"""
                        SELECT DISTINCT so.id, so.name, so.is_enabled, so.topic_id FROM stage_option so
                        JOIN stage_option_dependency sod ON so.id = sod.child_option_id
                        WHERE sod.parent_option_id IN ({selected_option_ids_placeholder}) AND so.stage_id = %s
                    """, tuple(selected_option_ids + [next_stage_id]))
                    next_stage_options = cursor.fetchall()

                    # Формируем список словарей для удобства работы с данными
                    return [{"id": opt[0], "name": opt[1], "is_enabled": opt[2], "topic_id": opt[3]} for opt in
                            next_stage_options]
        except Exception as error:
            print(f"Ошибка при получении опций для следующего шага: {error}")
            return []
