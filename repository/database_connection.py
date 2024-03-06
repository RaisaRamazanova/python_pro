import psycopg2


class DatabaseConnection:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(**self.db_config)
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Ошибка при подключении к базе данных: {error}")
                self.connection = None
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
