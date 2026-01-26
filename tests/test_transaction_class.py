import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import data.database as database
from helpers.transactions import (
    Transaction,
    format_currency,
    calculate_total_expenses,
    calculate_total_income,
    calculate_balance,
    check_financial_health,
    Base,
)


@pytest.fixture()
def session_factory(monkeypatch):
    """Use an in-memory SQLite database so tests are isolated and fast."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Patch the shared database module so application code uses this engine/session
    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(database, "SessionLocal", SessionLocal)

    Base.metadata.create_all(bind=engine)
    yield SessionLocal
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(session_factory):
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_transactions(db_session):
    """Create sample transactions in the database."""
    transactions = [
        Transaction(
            date="2024-01-01",
            description="Salary",
            amount=Decimal("10000.00"),
            category="Income",
        ),
        Transaction(
            date="2024-01-02",
            description="Groceries",
            amount=Decimal("-500.00"),
            category="Food",
        ),
        Transaction(
            date="2024-01-03",
            description="Rent",
            amount=Decimal("-4000.00"),
            category="Housing",
        ),
        Transaction(
            date="2024-01-04",
            description="Freelance",
            amount=Decimal("1500.00"),
            category="Income",
        ),
        Transaction(
            date="2024-01-05",
            description="Dinner",
            amount=Decimal("-250.50"),
            category="Food",
        ),
    ]
    for t in transactions:
        db_session.add(t)
    db_session.commit()
    return transactions


@pytest.fixture
def income_only_transactions(db_session):
    """Create income-only transactions in the database."""
    transactions = [
        Transaction(
            date="2024-01-01",
            description="Salary",
            amount=Decimal("3000.00"),
            category="Income",
        ),
        Transaction(
            date="2024-01-02",
            description="Bonus",
            amount=Decimal("500.00"),
            category="Income",
        ),
    ]
    for t in transactions:
        db_session.add(t)
    db_session.commit()
    return transactions


@pytest.fixture
def expenses_only_transactions(db_session):
    """Create expenses-only transactions in the database."""
    transactions = [
        Transaction(
            date="2024-01-01",
            description="Groceries",
            amount=Decimal("-200.00"),
            category="Food",
        ),
        Transaction(
            date="2024-01-02",
            description="Rent",
            amount=Decimal("-800.00"),
            category="Housing",
        ),
    ]
    for t in transactions:
        db_session.add(t)
    db_session.commit()
    return transactions


def test_invalid_amount():
    """Test that invalid amount raises ValueError."""
    with pytest.raises(ValueError):
        Transaction(
            date="2024-01-01", description="Invalid", amount="abc", category="Error"
        )


def test_format_currency():
    """Test currency formatting."""
    assert format_currency(Decimal("123.456")) == "R 123.46"
    assert format_currency(Decimal("-50.00")) == "R -50.00"


def test_calculate_total_expenses(sample_transactions):
    """Test calculating total expenses from a list of transactions."""
    assert calculate_total_expenses(sample_transactions) == Decimal("-4750.50")


def test_calculate_total_income(sample_transactions):
    """Test calculating total income from a list of transactions."""
    assert calculate_total_income(sample_transactions) == Decimal("11500.00")


def test_calculate_balance(sample_transactions):
    """Test calculating the balance from a list of transactions."""
    assert calculate_balance(sample_transactions) == Decimal("6749.50")


def test_empty_transactions():
    empty_list = []
    assert calculate_total_expenses(empty_list) == Decimal("0")
    assert calculate_total_income(empty_list) == Decimal("0")
    assert calculate_balance(empty_list) == Decimal("0")
    assert (
        check_financial_health(empty_list) == "No transactions recorded"
    )  # Since income is 0


def test_only_expenses(expenses_only_transactions):
    assert calculate_total_expenses(expenses_only_transactions) == Decimal("-1000.00")
    assert calculate_total_income(expenses_only_transactions) == Decimal("0")
    assert calculate_balance(expenses_only_transactions) == Decimal("-1000.00")
    assert check_financial_health(expenses_only_transactions) == "Overspending"


def test_only_income(income_only_transactions):
    assert calculate_total_expenses(income_only_transactions) == Decimal("0")
    assert calculate_total_income(income_only_transactions) == Decimal("3500.00")
    assert calculate_balance(income_only_transactions) == Decimal("3500.00")
    assert check_financial_health(income_only_transactions) == "No expenses recorded"


def test_mixed_transactions(sample_transactions):
    assert calculate_total_expenses(sample_transactions) == Decimal("-4750.50")
    assert calculate_total_income(sample_transactions) == Decimal("11500.00")
    assert calculate_balance(sample_transactions) == Decimal("6749.50")
    assert check_financial_health(sample_transactions) == "Saving well"
