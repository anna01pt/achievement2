
class DuplicateNumberError(Exception):
    pass


class SequenceError(Exception):
    pass


class InvalidNumberError(Exception):
    pass


class NumberService:

    def __init__(self, database, max_number=1_000_000):
        self.database = database
        self.max_number = max_number

    def process(self, number):

        if isinstance(number, bool) or not isinstance(number, int):
            raise InvalidNumberError("Ожидается целое число")

        if number < 0 or number > self.max_number:
            raise InvalidNumberError("Число вне допустимого диапазона")

        result = self.database.process_number(number)

        if result == "DUPLICATE":
            raise DuplicateNumberError(
                f"Число {number} уже поступало"
            )

        if result == "SEQUENCE_ERROR":
            raise SequenceError(
                f"Число {number} на единицу меньше уже обработанного"
            )

        return number + 1
