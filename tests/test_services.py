import json

import pytest
import pandas as pd
from src.services import search_transactions, search_phone_numbers, search_personal_transfers, safe_lower


def test_safe_lower():
    assert safe_lower("ТЕКСТ") == "текст"
    assert safe_lower(None) == ""
    assert safe_lower("") == ""


def test_search_transactions(test_transactions):
    global transactions
    transactions = test_transactions

    result = search_transactions("МТС")
    expected = [
        {"Описание": "Я МТС +7 921 11-22-33", "Категория": "Оплата"},
        {"Описание": "МТС Mobile +7 981 333-44-55", "Категория": "Оплата"},
    ]
    assert json.loads(result) == expected


def test_search_phone_numbers(test_transactions):
    global transactions
    transactions = test_transactions

    result = search_phone_numbers()
    expected = [
        {"Описание": "Я МТС +7 921 11-22-33", "Категория": "Оплата"},
        {"Описание": "Тинькофф Мобайл +7 995 555-55-55", "Категория": "Оплата"},
        {"Описание": "МТС Mobile +7 981 333-44-55", "Категория": "Оплата"},
    ]
    assert json.loads(result) == expected


def test_search_personal_transfers(test_transactions):
    global transactions
    transactions = test_transactions

    result = search_personal_transfers()
    expected = [
        {"Описание": "Перевод Валерий А. 1000 рублей", "Категория": "Переводы"},
        {"Описание": "Перевод Сергей З. 500 рублей", "Категория": "Переводы"},
        {"Описание": "Перевод Артем П. 200 рублей", "Категория": "Переводы"},
    ]

    assert json.loads(result) == expected
