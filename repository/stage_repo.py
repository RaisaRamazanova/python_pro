class StageRepository:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_all(self):
        """Возвращает список всех этапов из базы данных."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "SELECT id, name, index, is_required, description, is_enabled FROM stage"
            cursor.execute(query)
            stages = cursor.fetchall()
            cursor.close()
            return stages
        except Exception as error:
            print(f"Ошибка при получении всех этапов: {error}")
            return None

    def get_stage_details_by_id(self, stage_id):
        """Возвращает название и описание этапа по stage_id из таблицы stage"""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "SELECT name, description FROM stage WHERE stage_id = %s"
            cursor.execute(query, (stage_id,))
            stage_details = cursor.fetchone()  # Получаем первую запись, соответствующую stage_id
            cursor.close()
            if stage_details:
                return {"name": stage_details[0], "description": stage_details[1]}
            else:
                return None
        except Exception as error:
            print(f"Ошибка при получении деталей этапа по ID {stage_id}: {error}")
            return None

    def get_stage_translate(self, stage_id, language_id):
        """Возвращает перевод для определенного этапа на указанном языке."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = """
            SELECT description
            FROM stage_language
            WHERE stage_id = %s AND language_id = %s
            """
            cursor.execute(query, (stage_id, language_id))
            translation = cursor.fetchone()
            cursor.close()
            return translation[0]
        except Exception as error:
            print(f"Ошибка при получении перевода для этапа {stage_id} на языке {language_id}: {error}")
            return None

    def get_stage_by_index(self, index):
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = """
                    SELECT id
                    FROM stage
                    WHERE index = %s
                    """
            cursor.execute(query, (str(index)))
            translation = cursor.fetchone()
            cursor.close()
            return translation
        except Exception as error:
            print(f"Ошибка при получении stage для index {index}: {error}")
            return None