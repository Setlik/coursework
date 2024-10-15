import json
import logging
import os

import pandas as pd
from dotenv import load_dotenv
from pandas import date_range

from src.utils import load_transactions_from_excel, greeting, get_currency_data, get_stock_data, date_range_time

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join(PATH_HOME, "logs", "views.log"),
                    filemode='w')
logger = logging.getLogger()

load_dotenv()
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")


def generate_json_response(date_time_str):
    """Генерация JSON-ответа на основе переданной даты."""
    start_date, end_date = date_range_time(date_time_str)
    transactions_df = load_transactions_from_excel('operation.xlsx')
    transactions_df['Дата операции'] = pd.to_datetime(transactions_df['Дата операции'], format='%d.%m.%Y %H:%M:%S',
                                                      errors='coerce')
    filtered_transactions = transactions_df[
        (transactions_df['Дата операции'] >= start_date) & (transactions_df['Дата операции'] <= end_date)]
    total_expenses = filtered_transactions['Сумма операции'].sum()
    cashback = filtered_transactions['Кэшбэк'].sum()
    last_four_digits = filtered_transactions['Номер карты'].iloc[0][-4:] if not filtered_transactions.empty else "0000"
    top_transactions = filtered_transactions.nlargest(5, 'Сумма операции')[
        ['Дата операции', 'Сумма операции', 'Описание']]
    top_transactions['Дата операции'] = top_transactions['Дата операции'].dt.strftime('%Y-%m-%d %H:%M:%S')
    top_transactions = top_transactions.to_dict(orient='records')
    response = {
        "greeting": greeting(),
        "transactions_summary": {
            "last_four_digits": last_four_digits,
            "total_expenses": total_expenses,
            "cashback": cashback
        },
        "top_transactions": top_transactions,
        "currency_rates": get_currency_data([]),
        "stock_prices": get_stock_data([])
    }
    return json.dumps(response, ensure_ascii=False, indent=4)

# # Пример использования функции
# if __name__ == "__main__":
#     stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
#     prices = get_stock_data(stocks)
#     print(prices)
