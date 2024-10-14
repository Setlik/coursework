import json
import logging
import os

from dotenv import load_dotenv

from src.utils import load_transactions_from_excel, greeting, get_currency_data, load_user_settings, get_stock_data

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join(PATH_HOME, "logs", "views.log"),
                    filemode='w')
logger = logging.getLogger()

load_dotenv()
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")


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
