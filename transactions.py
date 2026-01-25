from decimal import Decimal
from typing import List, Tuple


# Constants
CURRENCY_SYMBOL = "R"
TRANSACTION_TYPES = ["income", "expense"]


# TODO: Implement the function below
def format_currency(amount: Decimal) -> str:
    """
    Format a numeric amount as South African Rand currency.

    Args:
        amount: The amount to format as a float or Decimal.

    Returns:
        A formatted string with the Rand symbol and two decimal places.

    Example:
        >>> format_currency(Decimal("1234.56"))
        'R 1234.56'
    """
    return ""


# TODO Implement the function below, if the transaction type is not valid raise a ValueError, if the amount is negative raise a ValueError
def add_transaction(
    transactions: List[dict], description: str, amount: Decimal, transaction_type: str
) -> List[dict]:
    """
    Add a new transaction to the transaction list.

    Args:
        transactions: The current list of transactions.
        description: A description of the transaction.
        amount: The transaction amount (positive value).
        transaction_type: Either "income" or "expense".

    Returns:
        The updated transactions list.

    Raises:
        ValueError: If transaction_type is not valid or amount is negative.

    Example:
        >>> transactions = []
        >>> add_transaction(transactions, "Salary", Decimal("5000"), "income")
        [{'description': 'Salary', 'amount': Decimal('5000'), 'type': 'income'}]
    """
    return transactions

# TODO: Implement the function below
def calculate_balance(transactions: List[dict]) -> Decimal:
    """
    Calculate the current balance from a list of transactions.

    Income transactions add to the balance; expense transactions subtract.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        The calculated balance as a Decimal.

    Example:
        >>> transactions = [
        ...     {"amount": Decimal("5000"), "type": "income"},
        ...     {"amount": Decimal("1000"), "type": "expense"}
        ... ]
        >>> calculate_balance(transactions)
        Decimal('4000')
    """
    return Decimal(0)

# TODO: Implement the function below
def get_income_total(transactions: List[dict]) -> Decimal:
    """
    Calculate the total income from all transactions.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        The total income as a Decimal.
    """
    return Decimal(0)

# TODO: Implement the function below
def get_expense_total(transactions: List[dict]) -> Decimal:
    """
    Calculate the total expenses from all transactions.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        The total expenses as a Decimal.
    """
    return Decimal(0)

# TODO: Implement the function below
# NOTE: If the balance exceeds the budget limit, return False and a message indicating overspend in a tuple
# NOTE: Remember to use your format_currency function to format the amounts in the message
def check_budget(balance: Decimal, budget_limit: Decimal) -> Tuple[bool, str]:
    """
    Check if the current balance is within the budget limit.

    Args:
        balance: The current balance.
        budget_limit: The maximum allowed budget.

    Returns:
        A tuple of (is_within_budget, message).

    Example:
        >>> check_budget(Decimal("500"), Decimal("1000"))
        (True, 'Within budget. R 500.00 of R 1000.00 used.')
        >>> check_budget(Decimal("1500"), Decimal("1000"))
        (False, 'Budget exceeded! Overspent by R 500.00.')
    """
    return (True, "")

# TODO: Implement the function below, however you see fit
def display_transactions(transactions: List[dict]) -> None:
    """
    Display all transactions in a formatted table.

    Args:
        transactions: A list of transaction dictionaries.
    """
    pass

# Example usage
if __name__ == "__main__":
    # Example usage
    # transactions = []
    # add_transaction(transactions, "Salary", Decimal("5000"), "income")
    # add_transaction(transactions, "Groceries", Decimal("1500"), "expense")
    # add_transaction(transactions, "Freelance", Decimal("2000"), "income")
    # add_transaction(transactions, "Rent", Decimal("2500"), "expense")

    # display_transactions(transactions)

    # balance = calculate_balance(transactions)
    # print(f"\nCurrent Balance: {format_currency(balance)}")

    # budget_limit = Decimal("3000")
    # within_budget, message = check_budget(balance, budget_limit)
    # print(message)
    pass
