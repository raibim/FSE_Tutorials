import pytest
from decimal import Decimal
from transactions import (
    Transaction,
    format_currency,
    calculate_total_expenses,
    calculate_total_income,
    calculate_balance,
)


@pytest.fixture
def sample_transactions():
    return [
        Transaction("2024-01-01", "Salary", Decimal("10000.00"), "Income"),
        Transaction("2024-01-02", "Groceries", Decimal("-500.00"), "Food"),
        Transaction("2024-01-03", "Rent", Decimal("-4000.00"), "Housing"),
        Transaction("2024-01-04", "Freelance", Decimal("1500.00"), "Income"),
        Transaction("2024-01-05", "Dinner", Decimal("-250.50"), "Food"),
    ]


def test_transaction_creation():
    t = Transaction("2024-01-01", "Test", "100.00", "Test Category")
    assert t.date == "2024-01-01"
    assert t.description == "Test"
    assert t.amount == Decimal("100.00")
    assert t.category == "Test Category"


def test_invalid_amount():
    with pytest.raises(ValueError):
        Transaction("2024-01-01", "Invalid", "abc", "Error")


def test_format_currency():
    assert format_currency(Decimal("123.456")) == "R 123.46"
    assert format_currency(Decimal("-50.00")) == "R -50.00"


def test_calculate_total_expenses(sample_transactions):
    assert calculate_total_expenses(sample_transactions) == Decimal("-4750.50")


def test_calculate_total_income(sample_transactions):
    assert calculate_total_income(sample_transactions) == Decimal("11500.00")


def test_calculate_balance(sample_transactions):
    assert calculate_balance(sample_transactions) == Decimal("6749.50")
