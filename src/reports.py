import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

from src.decorators import report_decorator

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - (levelname)s - %(message)s',
    filename=os.path.join(PATH_HOME, "logs", "reports.log"),
    filemode='w')
logger = logging.getLogger()
file_path = os.path.join(PATH_HOME, "data", "operations.xlsx")
transactions = pd.read_excel(file_path)
transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], dayfirst=True)


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца"""
    logger.info('Фильтрация транзакций по категории: %s', category)
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    target_date = pd.to_datetime(date, dayfirst=True)
    filtered_transactions = transactions[transactions['Категория'] == category]
    three_months_ago = target_date - pd.DateOffset(months=3)
    mask = (filtered_transactions['Дата платежа'] < target_date) & (
        filtered_transactions['Дата платежа'] >= three_months_ago)

    result = filtered_transactions[mask]

    logger.info('Найдено %d транзакций за указанный период', len(result))

    return result

# # Пример вызова функции
# if __name__ == "__main__":
#     result = spending_by_category(transactions, category='Супермаркеты', date='31-12-2021')
#     print(result)
