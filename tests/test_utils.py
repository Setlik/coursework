import json
from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd

from src.utils import get_currency_data, get_stock_data, greeting, load_transactions_from_excel, load_user_settings


def test_greet_good_night():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2022, 1, 1, 1, 0, 0)  # 1:00 AM
        assert greeting() == "Доброй ночи"


def test_greet_good_morning():
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2022, 1, 1, 8, 0, 0)  # 8:00 AM
        assert greeting() == "Доброе утро"


def test_greet_good_day():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2022, 1, 1, 14, 0, 0)  # 2:00 PM
        assert greeting() == "Добрый день"


def test_greet_good_evening():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2022, 1, 1, 19, 0, 0)  # 7:00 PM
        assert greeting() == "Добрый вечер"


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
            "2021-01-01 10:05:00": {"1. open": "153", "2. high": "156", "3. low": "151", "4. close": "153"}
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = get_stock_data(["AAPL"])
    assert result == {"AAPL": 153.0}


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
