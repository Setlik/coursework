import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(sample_data):
    """Тестирование функции spending_by_category."""
    result = spending_by_category(sample_data, 'Супермаркеты', '2023-02-15')
    expected_data = {
        'Дата платежа': ['2023-01-01', '2023-01-15'],
        'Категория': ['Супермаркеты', 'Супермаркеты'],
        'Сумма операции': [100, 200]
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df['Дата платежа'] = pd.to_datetime(expected_df['Дата платежа'])
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

# def test_spending_by_category_no_results(sample_data):
#     """Тестирование функции spending_by_category без результатов."""
#     result = spending_by_category(sample_data, 'Переводы', '2022-01-01')
#     expected_df = pd.DataFrame(columns=sample_data.columns)
#     pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)
