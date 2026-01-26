from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import data.database as database
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




