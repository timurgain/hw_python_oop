import random
from datetime import datetime, timedelta

import pytest

try:
    import cash_calories_calculator
except ImportError:
    pass


@pytest.fixture
def init_limit():
    return 2500


@pytest.fixture
def data_records():
    amount = 150
    count = random.randint(30, 40)
    today_count = random.randint(5, 10)
    week_count = random.randint(5, 10) + today_count
    future_count = random.randint(5, 10)
    data = []
    for idx, _ in enumerate(range(count)):
        if idx < today_count:
            date = datetime.now()
        elif idx < week_count:
            date = datetime.now() - timedelta(days=random.randint(1, 6))
        elif idx < future_count + week_count:
            date = datetime.now() + timedelta(days=random.randint(1, 6))
        else:
            date = datetime(2019, 9, 1)
        data.append(cash_calories_calculator.Record(amount=amount, comment=f'Test {idx}', date=date.strftime('%d.%m.%Y')))
    random.shuffle(data)
    return data, today_count * amount, week_count * amount


@pytest.fixture
def negative_calories_remained():
    return 'Хватит есть!'


@pytest.fixture
def positive_calories_remained():
    def _positive_calories_remained(limit):
        return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {limit} кКал'
    return _positive_calories_remained


@pytest.fixture
def today_cash_remained():

    def _today_positively(currency):
        return f'На сегодня осталось {remained_dict[currency]} {currency_dict[currency]}'

    def _today_negatively(currency):
        return f'Денег нет, держись: твой долг - {remained_dict[currency]} {currency_dict[currency]}'

    def _today_cash_remained(remained, currency):
        if remained == 0:
            return 'Денег нет, держись'
        elif remained == 1:
            return _today_positively(currency)
        elif remained == -1:
            return _today_negatively(currency)

    currency_dict = {
        'usd': 'USD',
        'eur': 'Euro',
        'rub': 'руб'
    }
    remained_dict = {
        'usd': '5(.0|.00|)',
        'eur': '4.29',
        'rub': '300(.0|.00|)'
    }
    return _today_cash_remained


@pytest.fixture
def fixture_CashCalculator(init_limit, monkeypatch):
    result = cash_calories_calculator.CashCalculator(init_limit)
    if hasattr(cash_calories_calculator.CashCalculator, 'currencies'):
        monkeypatch.setattr(cash_calories_calculator.CashCalculator, "currencies", {
            'eur': ('Euro', 70),
            'usd': ('USD', 60),
            'rub': ('руб', 1),
        })
    elif hasattr(cash_calories_calculator.CashCalculator, 'CURRENCIES'):
        monkeypatch.setattr(cash_calories_calculator.CashCalculator, "CURRENCIES", {
            'eur': ('Euro', 70),
            'usd': ('USD', 60),
            'rub': ('руб', 1),
        })
    else:
        monkeypatch.setattr(cash_calories_calculator.CashCalculator, "EURO_RATE", 70)
        monkeypatch.setattr(cash_calories_calculator.CashCalculator, "USD_RATE", 60)
    return result
