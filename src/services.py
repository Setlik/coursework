import json
import logging
import os
import re

import pandas as pd

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join(PATH_HOME, "logs", "services.log"),
                    filemode='w')
logger = logging.getLogger()
file_path = os.path.join(PATH_HOME, "data", "operations.xlsx")
transactions = pd.read_excel(file_path)


def safe_lower(value):
    """Безопасное приведение строки к нижнему регистру."""
    if pd.isna(value):
        return ''
    return value.lower()


def search_transactions(query: str) -> str:
    """Поиск транзакций по строке."""
    logger.info(f"Поиск транзакций по запросу: {query}")
    result = list(
        filter(lambda t: (query.lower() in safe_lower(t['Описание']) if t['Описание'] else False) or (query.lower()
               in safe_lower(t['Категория']) if t['Категория'] else False), transactions))
    return json.dumps(result, ensure_ascii=False)


def search_phone_numbers(transactions: pd.DataFrame) -> str:
    """Поиск транзакций по телефонным номерам."""
    logger.info("Поиск транзакций по телефонным номерам")
    phone_pattern = r'\+?\d[\d\s-]{7,}'
    transactions_list = transactions.to_dict(orient='records')
    result = list(filter(lambda t: t['Описание'] is not None and re.search(phone_pattern, t['Описание'].lower()),
                         transactions_list))
    return json.dumps(result, ensure_ascii=False)


def search_personal_transfers(transactions: pd.DataFrame) -> str:
    """Поиск переводов физическим лицам."""
    logger.info("Поиск переводов физическим лицам")
    personal_transfer_pattern = r'[А-Яа-я]\s+[А-Яа-я]\.'
    result = [
        t for t in transactions.to_dict(orient='records')
        if safe_lower(t['Категория']) == 'переводы' and re.search(personal_transfer_pattern, safe_lower(t['Описание']))
    ]
    return json.dumps(result, ensure_ascii=False)
