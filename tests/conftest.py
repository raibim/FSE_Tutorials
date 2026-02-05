import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data import database
from helpers.transactions import Transaction, Category, Base


@pytest.fixture()
def session_factory(monkeypatch):
    """Use an in-memory SQLite database so tests are isolated and fast."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
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
    categories = [
        Category(name="Groceries"),
        Category(name="Job"),
    ]

    transactions = [
        Transaction(
            date="2024-01-01",
            description="Salary",
            amount=Decimal("10000.00"),
            category_ref=categories[1],
        ),
        Transaction(
            date="2024-01-02",
            description="PnP Shopping",
            amount=Decimal("-500.00"),
            category_ref=categories[0],
        ),
        Transaction(
            date="2024-01-04",
            description="Freelance",
            amount=Decimal("1500.00"),
            category_ref=categories[1],
        ),
    ]
    for c in categories:
        db_session.add(c)
    db_session.commit()
    for t in transactions:
        db_session.add(t)
    db_session.commit()
    return transactions
