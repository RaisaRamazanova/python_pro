import psycopg2


class LanguageRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_all_languages(self):
        try:
            connection = self.db_connection.get_connection()
            cursor = connection.cursor()

            query = "SELECT * FROM language"
            cursor.execute(query)

            languages = cursor.fetchall()

            cursor.close()

            return languages
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Ошибка при работе с базой данных: {error}")
            return None