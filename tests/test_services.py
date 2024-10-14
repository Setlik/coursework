from src.services import safe_lower, search_personal_transfers, search_phone_numbers


def test_safe_lower():
    assert safe_lower("ТЕКСТ") == "текст"
    assert safe_lower(None) == ""
    assert safe_lower("") == ""


# def test_search_transactions(test_transactions):
#     transactions = test_transactions
#     result = search_transactions(transactions)
#     assert result is not None


def test_search_phone_numbers(test_transactions):
    transactions = test_transactions
    result = search_phone_numbers(transactions)
    assert result is not None


def test_search_personal_transfers(test_transactions):
    transactions = test_transactions
    result = search_personal_transfers(transactions)
    assert result is not None
