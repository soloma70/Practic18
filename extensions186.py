import requests
import json
from config186 import keys

class ChangeException(Exception):
    pass

class Change:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise ChangeException(f'Нет смысла переводить одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ChangeException(f'У меня нет такой валюты - {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ChangeException(f'У меня нет такой валюты - {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ChangeException(f'Невозможное количество - {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base1 = json.loads(r.content)[keys[base]]
        total_base = str(round(float(total_base1)*amount, 2))
        return total_base
