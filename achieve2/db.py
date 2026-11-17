
import psycopg
from contextlib import contextmanager


class Database:

    def __init__(self, connection_string):
        self.connection_string = connection_string

    @contextmanager
    def transaction(self):
        with psycopg.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                yield cursor

    def process_number(self, number):

        with self.transaction() as cursor:

            # Проверка повторного числа
            cursor.execute(
                "SELECT 1 FROM processed_numbers WHERE number = %s",
                (number,)
            )

            if cursor.fetchone():
                return "DUPLICATE"

            # Проверка наличия следующего числа
            cursor.execute(
                "SELECT 1 FROM processed_numbers WHERE number = %s",
                (number + 1,)
            )

            if cursor.fetchone():
                return "SEQUENCE_ERROR"

            # Сохранение числа
            cursor.execute(
                "INSERT INTO processed_numbers(number) VALUES (%s)",
                (number,)
            )

            return "OK"
