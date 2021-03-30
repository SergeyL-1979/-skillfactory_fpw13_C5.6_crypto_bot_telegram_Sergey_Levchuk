import requests
import json
from config_bot import keys


class APIException(Exception):
    pass


class ConverterBot:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base} ')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать колличество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={quote_ticker}&base={base_ticker}')

        total_base = json.loads(r.content)['rates'][keys[quote]] * amount

        return total_base
