from config import keys
class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount, exchanges=None):
        try:
            keys[base] = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            keys[quote] = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if keys[base] == keys[quote]:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

