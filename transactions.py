from decimal import Decimal, InvalidOperation
from typing import List, Tuple

# Constants
CURRENCY_SYMBOL = "R"


class Transaction:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        try:
            self.amount = Decimal(amount)
        except InvalidOperation:
            raise ValueError(f"Invalid amount: {amount}")
        self.category = category

    def __repr__(self):
        return f"Transaction(date='{self.date}', description='{self.description}', amount={self.amount}, category='{self.category}')"


def calculate_total_expenses(transactions: List[Transaction]) -> Decimal:
    total = Decimal(0)
    for transaction in transactions:
        if transaction.amount < 0:
            total += transaction.amount
    return total
    """Calculates the total expenses from a list of transactions.

    Args:
        transactions: A list of Transaction objects.

    Returns:
        The total expenses as a Decimal (should be negative).
    Example:
        >>> transactions = [Transaction('2024-01-01', 'Groceries', '-500.00', 'Food'),
        ...                 Transaction('2024-01-02', 'Rent', '-1500.00', 'Housing')]
        >>> calculate_total_expenses(transactions)
        Decimal('-2000.00')
    """
    return Decimal(0)


def calculate_total_income(transactions: List[Transaction]) -> Decimal:
    total = Decimal(0)
    for transaction in transactions:
        if transaction.amount > 0:
            total += transaction.amount
    return total

    """Calculates the total income from a list of transactions.
    
    Args:   
        transactions: A list of Transaction objects.

    Returns:
        The total income as a Decimal (should be positive).
    """
    return Decimal(0)


# NOTE: This function is already complete - no changes needed here!
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
    return f"{CURRENCY_SYMBOL} {amount:,.2f}"


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
    if transaction_type.lower() not in TRANSACTION_TYPES:
        raise ValueError(f"Transaction type must be one of {TRANSACTION_TYPES}")

    if amount < 0:
        raise ValueError("Amount must be positive")

    transaction = {
        "description": description,
        "amount": amount,
        "type": transaction_type.lower(),
    }

    transactions.append(transaction)
    return transactions


def calculate_balance(transactions: List[dict]) -> Decimal:
    balance = calculate_total_income(transactions) + calculate_total_expenses(
        transactions
    )
    return balance
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
    balance = Decimal(0)

    for transaction in transactions:
        if transaction["type"] == "income":
            balance += transaction["amount"]
        elif transaction["type"] == "expense":
            balance -= transaction["amount"]

    return balance


def get_income_total(transactions: List[dict]) -> Decimal:
    """
    Calculate the total income from all transactions.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        The total income as a Decimal.
    """
    total = Decimal(0)
    for item in transactions:
        if item["type"] == "income":
            total += item["amount"]
    return total


def get_expense_total(transactions: List[dict]) -> Decimal:
    """
    Calculate the total expenses from all transactions.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        The total expenses as a Decimal.
    """
    total = Decimal(0)
    for item in transactions:
        if item["type"] == "expense":
            total += item["amount"]
    return total


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
    """
    if balance > budget_limit:
        overspend = balance - budget_limit
        message = f"Budget exceeded! Overspent by {format_currency(overspend)}."
        return (False, message)
    else:
        message = (
            f"Within budget. {format_currency(balance)} of "
            f"{format_currency(budget_limit)} used."
        )
        return (True, message)


def display_transactions(transactions: List[dict]) -> None:
    """
    Display all transactions in a formatted table.

    Args:
        transactions: A list of transaction dictionaries.
    """
    if not transactions:
        print("No transactions recorded yet.")
        return

    for transaction in transactions:
        print(
            f"{transaction['description']:<20} "
            f"{transaction['type']:<10} "
            f"{format_currency((transaction['amount'])):<15}"
        )
