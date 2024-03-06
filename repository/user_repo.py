

class UserRepository:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_language(self, chat_id):
        """Возвращает предпочитаемый язык пользователя по chat_id."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "SELECT language_id FROM \"user\" WHERE telegram_chat_id = %s"
            cursor.execute(query, (chat_id,))
            language = cursor.fetchone()
            cursor.close()
            return language[0] if language else None
        except Exception as error:
            print(f"Ошибка при получении языка пользователя: {error}")
            return None

    def get_user_language_code(self, chat_id):
        """Возвращает код языка пользователя по chat_id."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    # Объединяем таблицы `user` и `language` для получения кода языка напрямую
                    query = """
                    SELECT l.code 
                    FROM "user" u
                    JOIN language l ON u.language_id = l.id
                    WHERE u.telegram_chat_id = %s AND l.is_enabled = TRUE
                    """
                    cursor.execute(query, (chat_id,))
                    language_code = cursor.fetchone()
                    return language_code[0] if language_code else None
        except Exception as error:
            print(f"Ошибка при получении кода языка пользователя: {error}")
            return None

    def update_language(self, user_id, new_language):
        """Обновляет предпочитаемый язык пользователя."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "UPDATE \"user\" SET preferred_language = %s WHERE id = %s"
            cursor.execute(query, (new_language, user_id))
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Ошибка при обновлении языка пользователя: {error}")
            return False

    def create(self, telegram_id, telegram_username, first_name, last_name, language_id, telegram_chat_id, is_banned):
        """Создаёт нового пользователя."""
        try:
            with self.db_connection.get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """
                    INSERT INTO "user" 
                    (telegram_id, telegram_username, first_name, last_name, language_id, telegram_chat_id, is_banned) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """
                    cursor.execute(query, (telegram_id, telegram_username, first_name, last_name, language_id, telegram_chat_id, is_banned))
                    user_id = cursor.fetchone()[0]  # Получаем ID вставленной записи
                    connection.commit()
                    return True, user_id  # Возвращаем флаг успеха и ID нового пользователя
        except Exception as error:
            print(f"Ошибка при создании пользователя: {error}")
            # Возвращаем False и None, если операция не удалась
            return False, None

    def update(self, telegram_id, telegram_username, first_name, last_name, language_id, telegram_chat_id, is_banned):
        """Обновляет данные пользователя."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "UPDATE \"user\" SET telegram_id = %s, telegram_username = %s, first_name = %s, last_name = %s, language_id = %s, is_banned = %s WHERE telegram_chat_id = %s"
            cursor.execute(query, (telegram_id, telegram_username, first_name, last_name, language_id, is_banned, telegram_chat_id))
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Ошибка при обновлении пользователя: {error}")
            return False

    def ban(self, user_id):
        """Блокирует пользователя по его ID."""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "UPDATE \"user\" SET is_banned = TRUE WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Ошибка при блокировке пользователя: {error}")
            return False

    def get_user_id(self, telegram_id):
        """Возвращает user_id по telegram_id"""
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()
            query = "SELECT id FROM \"user\" WHERE telegram_id = %s"
            cursor.execute(query, (telegram_id,))
            user_id = cursor.fetchone()
            cursor.close()
            return user_id[0] if user_id else None
        except Exception as error:
            print(f"Ошибка при получении языка пользователя: {error}")
            return None
