import json
import requests
from datetime import datetime
import pytz


# Функция для приветствия в зависимости от времени суток
def greeting(current_time):
    if current_time.hour < 6:
        return "Доброй ночи"
    elif current_time.hour < 12:
        return "Доброе утро"
    elif current_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


# Функция для получения данных из user_settings.json
def load_user_settings():
    with open('user_settings.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# Функция для получения курсов валют
def get_currency_data(currencies):
    api_url = 'https://api.exchangerate-api.com/v4/latest/USD'  # Пример API для валют
    response = requests.get(api_url)
    data = response.json()

    rates = {currency: data['rates'].get(currency) for currency in currencies}
    return rates


# Функция для получения цен акций
def get_stock_data(stocks):
    stock_prices = {}
    for stock in stocks:
        api_url = f'https://api.example.com/stock/{stock}'  # Пример API для акций
        response = requests.get(api_url)
        data = response.json()
        stock_prices[stock] = data['latestPrice']
    return stock_prices


# Главная функция для генерации JSON-ответа
def generate_json_response(date_str):
    # Парсинг даты из строки
    input_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now(pytz.timezone('Europe/Moscow'))  # Замените на свой часовой пояс

    # Готовим ответ
    response = {
        "greeting": greeting(current_time),
        "transactions_summary": {
            "last_four_digits": "1234",
            "total_expenses": 1000,
            "cashback": 10  # 1000 / 100 = 10
        },
        "top_transactions": [
            {"amount": 500, "description": "Оплата заказа"},
            {"amount": 300, "description": "Оплата услуги"},
            # Добавьте 3 других транзакции
        ],
        "currency_rates": get_currency_data(load_user_settings()["user_currencies"]),
        "stock_prices": get_stock_data(load_user_settings()["user_stocks"])
    }

    return json.dumps(response, ensure_ascii=False, indent=4)