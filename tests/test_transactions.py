import pytest
from decimal import Decimal

from transactions import (
    format_currency,
    add_transaction,
    calculate_balance,
    get_income_total,
    get_expense_total,
    check_budget,
    display_transactions,
)


class TestFormatCurrency:
    def test_format_currency_basic(self):
        assert format_currency(Decimal("1234.56")) == "R 1,234.56"

    def test_format_currency_whole_number(self):
        assert format_currency(Decimal("1000")) == "R 1,000.00"

    def test_format_currency_zero(self):
        assert format_currency(Decimal("0")) == "R 0.00"

    def test_format_currency_small_amount(self):
        assert format_currency(Decimal("5.5")) == "R 5.50"


class TestAddTransaction:
    def test_add_transaction_income(self):
        transactions = []
        result = add_transaction(transactions, "Salary", Decimal("5000"), "income")
        assert len(result) == 1
        assert result[0]["description"] == "Salary"
        assert result[0]["amount"] == Decimal("5000")
        assert result[0]["type"] == "income"

    def test_add_transaction_expense(self):
        transactions = []
        result = add_transaction(transactions, "Groceries", Decimal("1500"), "expense")
        assert len(result) == 1
        assert result[0]["type"] == "expense"

    def test_add_transaction_invalid_type(self):
        transactions = []
        with pytest.raises(ValueError):
            add_transaction(transactions, "Test", Decimal("100"), "invalid")

    def test_add_transaction_negative_amount(self):
        transactions = []
        with pytest.raises(ValueError):
            add_transaction(transactions, "Test", Decimal("-100"), "income")

    def test_add_transaction_multiple(self):
        transactions = []
        add_transaction(transactions, "Salary", Decimal("5000"), "income")
        add_transaction(transactions, "Rent", Decimal("2500"), "expense")
        assert len(transactions) == 2


class TestCalculateBalance:
    def test_calculate_balance_basic(self):
        transactions = [
            {"amount": Decimal("5000"), "type": "income"},
            {"amount": Decimal("1000"), "type": "expense"},
        ]
        assert calculate_balance(transactions) == Decimal("4000")

    def test_calculate_balance_empty(self):
        assert calculate_balance([]) == Decimal("0")

    def test_calculate_balance_only_income(self):
        transactions = [{"amount": Decimal("5000"), "type": "income"}]
        assert calculate_balance(transactions) == Decimal("5000")

    def test_calculate_balance_only_expenses(self):
        transactions = [{"amount": Decimal("1000"), "type": "expense"}]
        assert calculate_balance(transactions) == Decimal("-1000")


class TestGetIncomeTotal:
    def test_get_income_total_basic(self):
        transactions = [
            {"amount": Decimal("5000"), "type": "income"},
            {"amount": Decimal("2000"), "type": "income"},
            {"amount": Decimal("1000"), "type": "expense"},
        ]
        assert get_income_total(transactions) == Decimal("7000")

    def test_get_income_total_empty(self):
        assert get_income_total([]) == Decimal("0")

    def test_get_income_total_no_income(self):
        transactions = [{"amount": Decimal("1000"), "type": "expense"}]
        assert get_income_total(transactions) == Decimal("0")


class TestGetExpenseTotal:
    def test_get_expense_total_basic(self):
        transactions = [
            {"amount": Decimal("1000"), "type": "expense"},
            {"amount": Decimal("2500"), "type": "expense"},
            {"amount": Decimal("5000"), "type": "income"},
        ]
        assert get_expense_total(transactions) == Decimal("3500")

    def test_get_expense_total_empty(self):
        assert get_expense_total([]) == Decimal("0")

    def test_get_expense_total_no_expenses(self):
        transactions = [{"amount": Decimal("5000"), "type": "income"}]
        assert get_expense_total(transactions) == Decimal("0")


class TestCheckBudget:
    def test_check_budget_within_limit(self):
        is_within, message = check_budget(Decimal("500"), Decimal("1000"))
        assert is_within is True
        assert "Within budget" in message
        assert "R 500.00" in message
        assert "R 1,000.00" in message

    def test_check_budget_exceeded(self):
        is_within, message = check_budget(Decimal("1500"), Decimal("1000"))
        assert is_within is False
        assert "Budget exceeded" in message
        assert "R 500.00" in message

    def test_check_budget_exactly_at_limit(self):
        is_within, message = check_budget(Decimal("1000"), Decimal("1000"))
        assert is_within is True

    def test_check_budget_zero_balance(self):
        is_within, message = check_budget(Decimal("0"), Decimal("1000"))
        assert is_within is True


class TestDisplayTransactions:
    def test_display_transactions_empty(self, capsys):
        display_transactions([])
        captured = capsys.readouterr()
        assert isinstance(captured.out, str)

    def test_display_transactions_with_data(self, capsys):
        transactions = [
            {"description": "Salary", "amount": Decimal("5000"), "type": "income"},
            {"description": "Rent", "amount": Decimal("2500"), "type": "expense"},
        ]
        display_transactions(transactions)
        captured = capsys.readouterr()
        assert isinstance(captured.out, str)