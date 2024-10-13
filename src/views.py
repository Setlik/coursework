import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join(PATH_HOME, "logs", "views.log"),
                    filemode='w')
logger = logging.getLogger()

load_dotenv()
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")


def greeting():
    """Функция для приветствия в зависимости от времени суток"""
    current_time = datetime.now()
    hour = current_time.hour
    if hour < 6:
        return "Доброй ночи"
    elif hour < 12:
        return "Доброе утро"
    elif hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def load_user_settings():
    """Функция для получения данных из user_settings.json"""
    with open('user_settings.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_currency_data(currencies=["USD", "EUR"]):
    """Функция получения стоимости валют по отношению к рублю"""
    api_key = {"apikey": API_KEY_CURRENCY}
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}]/latest/RUB"
    querystring = ','.join(currencies)
    response = requests.get(api_url, params=querystring)
    if response.status_code != 200:
        print("Error: Unable to fetch data")
        return {"error": "Unable to fetch data"}
    data = response.json()
    if 'conversion_rates' not in data:
        print("Error: Invalid data format")
        return {"error": "Invalid data format"}
    rates = {}
    for currency in currencies:
        rate = data['conversion_rates'].get(currency)
        if rate is not None:
            rates[currency] = rate
        else:
            print(f"Warning: Rate for currency {currency} not found.")
    return rates if rates else {"error": "No valid rates found"}


def get_stock_data(stocks):
    """Функция получения стоимости акций"""
    stock_prices = {}
    api_key = {"apikey": API_KEY_STOCK}
    for stock in stocks:
        api_url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='
                   f'{stock}&interval=5min&apikey={api_key}')
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            try:
                time_series = data['Time Series (5min)']
                latest_time = sorted(time_series.keys())[0]
                latest_data = time_series[latest_time]
                stock_prices[stock] = float(latest_data['4. close'])
            except KeyError:
                print(f"Ошибка: отсутствуют данные для {stock}. Ответ API: {data}")
                stock_prices[stock] = None
        else:
            print(f"Ошибка при запросе данных по акции {stock}: {response.status_code}")
            stock_prices[stock] = None

    return stock_prices


def load_transactions_from_excel(file_path):
    """Функция для загрузки транзакций из Excel файла"""
    path_to_xlsx = os.path.join(PATH_HOME, "data", "operations.xlsx")
    df = pd.read_excel(path_to_xlsx)
    return df


def generate_json_response():
    """Главная функция для генерации JSON-ответа"""
    transactions_df = load_transactions_from_excel('operation.xlsx')
    total_expenses = transactions_df['Сумма операции'].sum()
    cashback = transactions_df['Кэшбэк'].sum()
    last_four_digits = transactions_df['Номер карты'].iloc[0][-4:] if not transactions_df.empty else "0000"
    top_transactions = transactions_df.nlargest(5, 'Сумма операции')[
        ['Дата операции', 'Сумма операции', 'Описание']].to_dict(orient='records')
    response = {
        "greeting": greeting(),
        "transactions_summary": {
            "last_four_digits": last_four_digits,
            "total_expenses": total_expenses,
            "cashback": cashback
        },
        "top_transactions": top_transactions,
        "currency_rates": get_currency_data(load_user_settings().get("user_currencies", [])),
        "stock_prices": get_stock_data(load_user_settings().get("user_stocks", []))
    }

    return json.dumps(response, ensure_ascii=False, indent=4)

# # Пример использования функции
# if __name__ == "__main__":
#     stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     prices = get_stock_data(stocks)
#     print(prices)
