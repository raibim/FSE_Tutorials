"""Seed script to populate the database with initial data.

Run this script from the project root using:
    python -m data.seed
"""
from datetime import datetime
from decimal import Decimal

from helpers.transactions import Transaction, Category
from data.database import init_db, get_session


def seed_database():
    # Initialize database and create tables
    init_db()

    # Get a session
    session = get_session()

    try:
        # Check if the category exists before adding it
        income_category = session.query(Category).filter_by(name="Income").first()

        if not income_category:
            income_category = Category(name="Income")
            session.add(income_category)
            session.commit()  # Commit now so the ID is available
            print("Created new 'Income' category.")
        else:
            print("Using existing 'Income' category.")

        # Check if transactions exist, if not, create sample transactions
        existing_transactions = session.query(Transaction).first()
        if not existing_transactions:
            # Create sample transactions
            transactions = [
                Transaction(
                    date=datetime.now().isoformat(),
                    description="Salary",
                    amount=Decimal("5000"),
                    category="Income",
                    category_ref=income_category,
                ),
                Transaction(
                    date=datetime.now().isoformat(),
                    description="Freelance Project",
                    amount=Decimal("1500"),
                    category="Income",
                    category_ref=income_category,
                ),
                Transaction(
                    date=datetime.now().isoformat(),
                    description="Gift",
                    amount=Decimal("-2000"),
                    category="Expense",
                ),
            ]

            # Add transactions to session
            for transaction in transactions:
                session.add(transaction)
            print("Created and added sample transactions to the database.")
            session.commit()
        else:
            print("Transactions already exist in the database. No new transactions added.")

    finally:
        session.close()

if __name__ == "__main__":
    seed_database()