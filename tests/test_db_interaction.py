from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import data.database as database
from app import add_expense_category, add_expenses, display_transactions_by_category
from helpers.transactions import Base, Category, Transaction


@pytest.fixture()
def session_factory(monkeypatch):
	"""Use an in-memory SQLite database so tests stay isolated."""
	engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

	# Patch the database module so the app code uses the test engine/session
	monkeypatch.setattr(database, "engine", engine)
	monkeypatch.setattr(database, "SessionLocal", SessionLocal)

	Base.metadata.create_all(bind=engine)
	yield SessionLocal
	Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def session(session_factory):
	sess = session_factory()
	try:
		yield sess
	finally:
		sess.close()


def test_add_expense_category_creates_and_reuses(session):
	add_expense_category()
	add_expense_category()  # idempotent

	categories = session.query(Category).filter_by(name="Expense").all()
	assert len(categories) == 1


def test_add_expenses_inserts_sample_data(session):
	add_expense_category()
	add_expenses()

	expenses = session.query(Transaction).filter(Transaction.amount < 0).all()
	assert len(expenses) == 2
	assert all(exp.category_id is not None for exp in expenses)
	assert {str(exp.amount) for exp in expenses} == {"-600.00", "-300.00"}


def test_add_expenses_is_idempotent(session):
	add_expense_category()
	add_expenses()
	add_expenses()  # should detect existing expenses and skip

	expenses = session.query(Transaction).filter(Transaction.amount < 0).all()
	assert len(expenses) == 2


def test_display_transactions_by_category_outputs(capsys, session):
	income = Category(name="Income")
	session.add(income)
	session.add(
		Transaction(
			date="2024-02-01",
			description="Salary",
			amount=Decimal("5000"),
			category="Income",
			category_ref=income,
		)
	)
	session.commit()

	display_transactions_by_category("Income")
	captured = capsys.readouterr().out

	assert "Transactions in category 'Income':" in captured
	assert "Salary" in captured
