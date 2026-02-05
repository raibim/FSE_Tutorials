from decimal import Decimal

import pytest
from helpers.transactions import (
    Transaction,
    format_currency,
    calculate_total_expenses,
    calculate_total_income,
    calculate_balance,
    check_financial_health,
)


def test_invalid_amount():
    """Test that invalid amount raises ValueError."""
    with pytest.raises(ValueError):
        Transaction(
            date="2024-01-01", description="Invalid", amount="abc", category_ref=None
        )


def test_format_currency():
    """Test currency formatting."""
    assert format_currency(Decimal("123.456")) == "R 123.46"
    assert format_currency(Decimal("-50.00")) == "R -50.00"


def test_calculate_total_expenses(sample_transactions):
    """Test calculating total expenses from a list of transactions."""
    assert calculate_total_expenses(sample_transactions) == Decimal("-500.00")


def test_calculate_total_income(sample_transactions):
    """Test calculating total income from a list of transactions."""
    assert calculate_total_income(sample_transactions) == Decimal("11500.00")


def test_calculate_balance(sample_transactions):
    """Test calculating the balance from a list of transactions."""
    assert calculate_balance(sample_transactions) == Decimal("11000.00")


def test_empty_transactions():
    empty_list = []
    assert calculate_total_expenses(empty_list) == Decimal("0")
    assert calculate_total_income(empty_list) == Decimal("0")
    assert calculate_balance(empty_list) == Decimal("0")
    assert (
        check_financial_health(empty_list) == "No transactions recorded"
    )  # Since income is 0


def test_only_expenses(sample_transactions):
    sample_transactions = [t for t in sample_transactions if t.amount < 0]
    assert calculate_total_expenses(sample_transactions) == Decimal("-500.00")
    assert calculate_total_income(sample_transactions) == Decimal("0")
    assert calculate_balance(sample_transactions) == Decimal("-500.00")
    assert check_financial_health(sample_transactions) == "Overspending"


def test_only_income(sample_transactions):
    sample_transactions = [t for t in sample_transactions if t.amount > 0]
    assert calculate_total_expenses(sample_transactions) == Decimal("0")
    assert calculate_total_income(sample_transactions) == Decimal("11500.00")
    assert calculate_balance(sample_transactions) == Decimal("11500.00")
    assert check_financial_health(sample_transactions) == "No expenses recorded"


def test_mixed_transactions(sample_transactions):
    assert calculate_total_expenses(sample_transactions) == Decimal("-500.00")
    assert calculate_total_income(sample_transactions) == Decimal("11500.00")
    assert calculate_balance(sample_transactions) == Decimal("11000.00")
    assert check_financial_health(sample_transactions) == "Saving well"
