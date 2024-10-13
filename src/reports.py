import json
import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join(PATH_HOME, "logs", "reports.log"),
                    filemode='w')
logger = logging.getLogger()
file_path = os.path.join(PATH_HOME, "data", "operations.xlsx")
transactions = pd.read_excel(file_path)
transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], dayfirst=True)


def report_decorator(filename: Optional[str] = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            file_name = filename if filename else 'report.json'
            result_json = result.copy()
            if 'Дата платежа' in result_json.columns:
                result_json['Дата платежа'] = result_json['Дата платежа'].dt.strftime('%Y-%m-%d')
            result_dict = result_json.to_dict(orient='records')
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, ensure_ascii=False, indent=4)
            logging.info(f'Отчет записан в файл: {file_name}')
            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    target_date = pd.to_datetime(date, dayfirst=True)
    filtered_transactions = transactions[transactions['Категория'] == category]
    three_months_ago = target_date - pd.DateOffset(months=3)
    mask = (filtered_transactions['Дата платежа'] < target_date) & (
            filtered_transactions['Дата платежа'] >= three_months_ago)
    return filtered_transactions[mask]


# # Пример вызова функции
# result = spending_by_category(transactions, category='Супермаркеты', date='31-12-2021')
# print(result)
