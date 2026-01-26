from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import data.database as database
from app import display_transactions_by_category
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
