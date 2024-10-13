import datetime
from unittest.mock import patch, mock_open

import pytest
import json
import os
import pandas as pd

from src.views import generate_json_response, load_transactions_from_excel, get_stock_data, get_currency_data, \
    load_user_settings, greeting


# Тест функции greeting
def test_greeting(monkeypatch):
    monkeypatch.setattr('datetime.datetime.now', lambda: datetime.datetime(2021, 1, 1, 5, 0))
    assert greeting() == "Доброе утро"
    monkeypatch.setattr('datetime.datetime.now', lambda: datetime.datetime(2021, 1, 1, 13, 0))
    assert greeting() == "Добрый день"


def test_load_user_settings():
    mock_data = json.dumps({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]})
    with patch("builtins.open", mock_open(read_data=mock_data)):
        settings = load_user_settings()
        assert settings == {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "TSLA"]}


@patch('requests.get')
def test_get_currency_data(mock_get):
    mock_response = {
        "conversion_rates": {
            "USD": 74.95,
            "EUR": 88.22
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = get_currency_data(["USD", "EUR"])
    assert result == {"USD": 74.95, "EUR": 88.22}


@patch('requests.get')
def test_get_currency_data_invalid_format(mock_get):
    mock_response = {"invalid": "data"}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = get_currency_data(["USD", "EUR"])
    assert result == {"error": "Invalid data format"}


@patch('requests.get')
def test_get_stock_data(mock_get):
    mock_response = {
        "Time Series (5min)": {
            "2021-01-01 10:00:00": {"1. open": "150", "2. high": "155", "3. low": "149", "4. close": "153"},
            "2021-01-01 10:05:00": {"1. open": "153", "2. high": "156", "3. low": "151", "4. close": "154"}
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = get_stock_data(["AAPL"])
    assert result == {"AAPL": 154.0}


@patch('pandas.read_excel')
def test_load_transactions_from_excel(mock_read_excel):
    mock_df = pd.DataFrame({
        "Сумма операции": [100, 200],
        "Кэшбэк": [5, 10],
        "Номер карты": ["1234 5678 9012 3456", "1234 5678 9012 3456"],
        "Дата операции": ["2021-01-01", "2021-01-02"],
        "Описание": ["Покупка", "Покупка"]
    })
    mock_read_excel.return_value = mock_df

    transactions = load_transactions_from_excel("dummy_path.xlsx")
    assert transactions.equals(mock_df)


@patch('your_module_name.load_transactions_from_excel')
@patch('your_module_name.get_currency_data')
@patch('your_module_name.get_stock_data')
@patch('your_module_name.load_user_settings')
def test_generate_json_response(mock_load_user_settings, mock_get_stock_data, mock_get_currency_data,
                                mock_load_transactions_from_excel):
    mock_load_user_settings.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_load_transactions_from_excel.return_value = pd.DataFrame({
        "Сумма операции": [100, 200],
        "Кэшбэк": [5, 10],
        "Номер карты": ["1234 5678 9012 3456", "1234 5678 9012 3456"],
        "Дата операции": ["2021-01-01", "2021-01-02"],
        "Описание": ["Покупка", "Покупка"]
    })
    mock_get_currency_data.return_value = {"USD": 74.95}
    mock_get_stock_data.return_value = {"AAPL": 154.0}

    response = generate_json_response()
    expected_response = {
        "greeting": greeting(),
        "transactions_summary": {
            "last_four_digits": "3456",
            "total_expenses": 300,
            "cashback": 15
        },
        "top_transactions": [
            {"Дата операции": "2021-01-01", "Сумма операции": 100, "Описание": "Покупка"},
            {"Дата операции": "2021-01-02", "Сумма операции": 200, "Описание": "Покупка"}
        ],
        "currency_rates": {"USD": 74.95},
        "stock_prices": {"AAPL": 154.0}
    }

    assert json.loads(response) == expected_response