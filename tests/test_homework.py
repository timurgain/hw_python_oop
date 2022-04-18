import re
import inspect
from typing import Optional
from datetime import datetime

import pytest

try:
    import cash_calories_calculator
except ModuleNotFoundError:
    assert False, 'Не найдена домашняя работа'


class TestRecord:
    init_records = [{'amount': 1000, 'comment': 'Тестовый коммент'},
                    {'amount': 1000, 'comment': 'Тестовый коммент', 'date': '01.09.2019'}]

    @pytest.mark.parametrize("kwargs", init_records)
    def test_init(self, kwargs, msg_err):
        assert hasattr(cash_calories_calculator, 'Record'), msg_err('add_class', 'Record')
        result = cash_calories_calculator.Record(**kwargs)
        assert hasattr(result, 'amount'), msg_err('add_attr', 'amount', 'Record')
        assert result.amount == kwargs['amount'], msg_err('wrong_attr', 'amount', 'Record')
        assert hasattr(result, 'comment'), msg_err('add_attr', 'comment', 'Record')
        assert result.comment == kwargs.get('comment', ''), msg_err('wrong_attr', 'comment', 'Record')
        assert hasattr(result, 'date'), msg_err('add_attr', 'date', 'Record')
        if 'date' in kwargs:
            date_standard_default_annotation_arg = inspect.Parameter(
                'date',
                inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=Optional[str],
            )
            date_future_default_annotation_arg = inspect.Parameter(
                'date',
                inspect.Parameter.KEYWORD_ONLY,
                annotation='Optional[str]',
                default=None,
            )
            date_default_arg = inspect.Parameter(
                'date',
                inspect.Parameter.KEYWORD_ONLY,
                default=None,
            )
            inspect_signature = str(inspect.signature(cash_calories_calculator.Record).parameters['date'])
            assert any([inspect_signature == str(arg) for arg in (date_standard_default_annotation_arg,
                                                             date_future_default_annotation_arg,
                                                             date_default_arg)]), \
                (
                'В качестве дефолтного аргумента для даты '
                'не должно быть посчитанное значение или пустая строка'
            )
            assert result.date == datetime.strptime(kwargs['date'], '%d.%m.%Y').date(), (
                msg_err('wrong_attr', 'date', 'Record', ', свойство должно быть датой')
            )
        else:
            assert result.date == datetime.now().date(), (
                msg_err('wrong_attr', 'date', 'Record', ', свойство должно быть датой')
            )

        assert not hasattr(result, 'USD_RATE'), msg_err('dont_create_attr', 'USD_RATE', 'Record')
        assert not hasattr(result, 'EURO_RATE'), msg_err('dont_create_attr', 'EURO_RATE', 'Record')


class TestCalculator:

    def test_init(self, init_limit, msg_err):
        assert hasattr(cash_calories_calculator, 'Calculator'), msg_err('add_class', 'Calculator')
        result = cash_calories_calculator.Calculator(init_limit)
        assert hasattr(result, 'limit'), msg_err('add_attr', 'limit', 'Calculator')
        assert result.limit == init_limit, msg_err('wrong_attr', 'limit', 'Calculator')
        assert hasattr(result, 'records'), msg_err('add_attr', 'records', 'Calculator')
        assert result.records == [], msg_err('wrong_attr', 'records', 'Calculator')

        assert not hasattr(result, 'USD_RATE'), msg_err('dont_create_attr', 'USD_RATE', 'Calculator')
        assert not hasattr(result, 'EURO_RATE'), msg_err('dont_create_attr', 'EURO_RATE', 'Calculator')

    def test_add_record(self, init_limit, data_records, msg_err):
        result = cash_calories_calculator.Calculator(init_limit)
        assert hasattr(result, 'add_record'), msg_err('add_method', 'add_record', 'Calculator')
        records, today, week = data_records
        for record in records:
            result.add_record(record)
        assert result.records == records, msg_err('wrong_attr', 'records', 'Calculator')

    def test_get_today_stats(self, init_limit, data_records, msg_err):
        result = cash_calories_calculator.Calculator(init_limit)
        records, today, week = data_records
        for record in records:
            result.add_record(record)
        assert hasattr(result, 'get_today_stats'), msg_err('add_method', 'get_today_stats', 'Calculator')
        assert result.get_today_stats() == today, msg_err('wrong_method', 'get_today_stats', 'Calculator')

    def test_get_week_stats(self, init_limit, data_records, msg_err):
        result = cash_calories_calculator.Calculator(init_limit)
        records, today, week = data_records
        for record in records:
            result.add_record(record)
        assert hasattr(result, 'get_week_stats'), msg_err('add_method', 'get_week_stats', 'Calculator')
        assert result.get_week_stats() == week, msg_err('wrong_method', 'get_week_stats', 'Calculator')
        get_week_stats_inspect = inspect.getsource(result.get_week_stats)
        get_week_stats_inspect_in_class = inspect.getsource(cash_calories_calculator.Calculator)
        assert (
            'days=7' in get_week_stats_inspect or
            'weeks=1' in get_week_stats_inspect or
            'days=7' in get_week_stats_inspect_in_class or
            'weeks=1' in get_week_stats_inspect_in_class
        ), 'Необходимо считать сколько денег потрачено за последние 7 дней'

    def test_get_calories_remained(self, init_limit, msg_err):
        result = cash_calories_calculator.Calculator(init_limit)
        assert not hasattr(result, 'get_calories_remained'), (
            msg_err('dont_create_method', 'get_calories_remained', 'Calculator')
        )

    def test_get_today_cash_remained(self, init_limit, msg_err):
        result = cash_calories_calculator.Calculator(init_limit)
        assert not hasattr(result, 'get_today_cash_remained'), (
            msg_err('dont_create_method', 'get_today_cash_remained', 'Calculator')
        )


class TestCaloriesCalculator:

    def test_init(self, init_limit, msg_err):
        assert hasattr(cash_calories_calculator, 'CaloriesCalculator'), (
            msg_err('add_class', 'CaloriesCalculator', child=True, parent_name='Calculator')
        )
        result = cash_calories_calculator.CaloriesCalculator(init_limit)
        assert hasattr(result, 'limit'), msg_err('child_method', 'CaloriesCalculator', 'Calculator')
        assert result.limit == init_limit, msg_err('child_method', 'CaloriesCalculator', 'Calculator')

        assert not hasattr(result, 'USD_RATE'), msg_err('dont_create_attr', 'USD_RATE', 'CaloriesCalculator')
        assert not hasattr(result, 'EURO_RATE'), msg_err('dont_create_attr', 'EURO_RATE', 'CaloriesCalculator')

    def test_get_calories_remained(self, init_limit, data_records,
                                   negative_calories_remained, positive_calories_remained, msg_err):
        result = cash_calories_calculator.CaloriesCalculator(init_limit)
        assert hasattr(result, 'get_calories_remained'), (
            msg_err('add_method', 'get_calories_remained', 'CaloriesCalculator')
        )

        records, today, week = data_records
        for record in records:
            result.add_record(record)

        if today < init_limit:
            assert result.get_calories_remained() == positive_calories_remained(init_limit - today), (
                msg_err('wrong_method', 'get_calories_remained', 'CaloriesCalculator')
            )
            result.limit = today - 200
            assert result.get_calories_remained() == negative_calories_remained, (
                msg_err('wrong_method', 'get_calories_remained', 'CaloriesCalculator')
            )
        else:
            assert result.get_calories_remained() == negative_calories_remained, (
                msg_err('wrong_method', 'get_calories_remained', 'CaloriesCalculator')
            )
            result.limit = today + 200
            assert result.get_calories_remained() == positive_calories_remained(init_limit - today), (
                msg_err('wrong_method', 'get_calories_remained', 'CaloriesCalculator')
            )


class TestCashCalculator:

    def test_init(self, init_limit, msg_err):
        assert hasattr(cash_calories_calculator, 'CashCalculator'), (
            msg_err('add_class', 'CashCalculator', child=True, parent_name='Calculator')
        )
        result = cash_calories_calculator.CashCalculator(init_limit)
        assert hasattr(result, 'limit'), msg_err('child_method', 'CashCalculator', 'Calculator')
        assert result.limit == init_limit, msg_err('child_method', 'CashCalculator', 'Calculator')

        assert hasattr(result, 'EURO_RATE'), msg_err('add_attr', 'EURO_RATE', 'CashCalculator')
        assert type(result.EURO_RATE) == float, msg_err('wrong_attr', 'EURO_RATE', 'CashCalculator')
        assert result.EURO_RATE > 0, msg_err('wrong_attr', 'EURO_RATE', 'CashCalculator',
                                             msg=', курс не может быть равен или меньше 0')

        assert hasattr(result, 'USD_RATE'), msg_err('add_attr', 'USD_RATE', 'CashCalculator')
        assert type(result.USD_RATE) == float, msg_err('wrong_attr', 'USD_RATE', 'CashCalculator')
        assert result.USD_RATE > 0, msg_err('wrong_attr', 'USD_RATE', 'CashCalculator',
                                            msg=', курс не может быть равен или меньше 0')

    @pytest.mark.parametrize("amount,currency", [
        (0, 'usd'), (0, 'eur'), (0, 'rub'),
        (1, 'usd'), (1, 'eur'), (1, 'rub'),
        (-1, 'usd'), (-1, 'eur'), (-1, 'rub')
    ])
    def test_get_today_cash_remained(self, data_records, amount, currency, today_cash_remained, msg_err, monkeypatch, fixture_CashCalculator):
        result = fixture_CashCalculator
        assert hasattr(result, 'get_today_cash_remained'), (
            msg_err('add_method', 'get_today_cash_remained', 'CashCalculator')
        )

        records, today, week = data_records
        for record in records:
            result.add_record(record)

        result.limit = today + (amount * 300)
        assert re.fullmatch(today_cash_remained(amount, currency), result.get_today_cash_remained(currency)), (
            msg_err('wrong_method', 'get_today_cash_remained', 'CashCalculator')
        )
