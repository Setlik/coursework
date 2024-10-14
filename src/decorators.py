import json
import logging
import os
from typing import Optional

PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join(PATH_HOME, "logs", "reports.log"),
                    filemode='w')
logger = logging.getLogger()


def report_decorator(filename: Optional[str] = None):
    """Декоратор для функций-отчетов, который записывает в файл результат, который возвращает функция"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info('Запуск функции: %s', func.__name__)
            result = func(*args, **kwargs)
            file_name = filename if filename else 'report.json'
            result_json = result.copy()
            if 'Дата платежа' in result_json.columns:
                result_json['Дата платежа'] = result_json['Дата платежа'].dt.strftime('%Y-%m-%d')
            result_dict = result_json.to_dict(orient='records')
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, ensure_ascii=False, indent=4)
            logger.info(f'Отчет записан в файл: {file_name}')
            return result

        return wrapper

    return decorator
