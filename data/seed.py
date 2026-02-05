"""Seed script to populate the database with initial data.

Run this script from the project root using:
    python -m data.seed
"""

from datetime import datetime
from decimal import Decimal
from datetime import timedelta

from loguru import logger
from helpers.transactions import Transaction, Category
from data.database import init_db, get_session


def create_or_get_category(session, category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        session.add(category)
        session.commit()
    return category


def seed_database():
    # Initialize database and create tables
    init_db()

    # Get a session
    session = get_session()

    try:
        # Check if the category exists before adding it
        job_cat = create_or_get_category(session, "Job")
        side_business_cat = create_or_get_category(session, "Side Business")
        groceries_cat = create_or_get_category(session, "Groceries")
        entertainment_cat = create_or_get_category(session, "Entertainment")
        housing_cat = create_or_get_category(session, "Housing")
        utilities_cat = create_or_get_category(session, "Utilities")
        health_cat = create_or_get_category(session, "Health")
        car_cat = create_or_get_category(session, "Car")
        misc_cat = create_or_get_category(session, "Miscellaneous")

        # Add transactions
        transactions = [
            # --- JANUARY 2026 ---
            Transaction(
                date=days_ago(1),
                description="Monthly Salary",
                amount=Decimal("35000.00"),
                category_ref=job_cat,
            ),
            Transaction(
                date=days_ago(3),
                description="Pick n Pay Groceries",
                amount=Decimal("-1250.50"),
                category_ref=groceries_cat,
            ),
            Transaction(
                date=days_ago(5),
                description="Rent Payment",
                amount=Decimal("-12000.00"),
                category_ref=housing_cat,
            ),
            Transaction(
                date=days_ago(10),
                description="Freelance Project: Web Design",
                amount=Decimal("4500.00"),
                category_ref=side_business_cat,
            ),
            Transaction(
                date=days_ago(12),
                description="Electricity/Water Bill",
                amount=Decimal("-1850.00"),
                category_ref=utilities_cat,
            ),
            Transaction(
                date=days_ago(15),
                description="Netflix Subscription",
                amount=Decimal("-199.00"),
                category_ref=entertainment_cat,
            ),
            Transaction(
                date=days_ago(18),
                description="Petrol Station",
                amount=Decimal("-950.00"),
                category_ref=car_cat,
            ),
            Transaction(
                date=days_ago(22),
                description="Dinner with Friends",
                amount=Decimal("-650.00"),
                category_ref=entertainment_cat,
            ),
            # --- DECEMBER 2025 ---
            Transaction(
                date=days_ago(27),
                description="Year-End Bonus",
                amount=Decimal("15000.00"),
                category_ref=job_cat,
            ),
            Transaction(
                date=days_ago(28),
                description="Monthly Salary",
                amount=Decimal("35000.00"),
                category_ref=job_cat,
            ),
            Transaction(
                date=days_ago(32),
                description="Holiday Gift Shopping",
                amount=Decimal("-4200.00"),
                category_ref=misc_cat,
            ),
            Transaction(
                date=days_ago(35),
                description="Rent Payment",
                amount=Decimal("-12000.00"),
                category_ref=housing_cat,
            ),
            Transaction(
                date=days_ago(40),
                description="Checkers Groceries",
                amount=Decimal("-1100.25"),
                category_ref=groceries_cat,
            ),
            Transaction(
                date=days_ago(45),
                description="Internet Fiber Line",
                amount=Decimal("-899.00"),
                category_ref=utilities_cat,
            ),
            Transaction(
                date=days_ago(50),
                description="Coffee Shop",
                amount=Decimal("-45.00"),
                category_ref=entertainment_cat,
            ),
            Transaction(
                date=days_ago(55),
                description="Gym Membership",
                amount=Decimal("-550.00"),
                category_ref=health_cat,
            ),
            Transaction(
                date=days_ago(60),
                description="Freelance Project: Logo",
                amount=Decimal("2200.00"),
                category_ref=side_business_cat,
            ),
        ]
        add_transactions(session, transactions)
    finally:
        session.close()


# Helper to generate dates relative to today (Jan 26, 2026)
def days_ago(n):
    return (datetime.now() - timedelta(days=n)).isoformat()


def add_transactions(session, transactions):
    for t in transactions:
        session.add(t)
    session.commit()
    logger.info(f"Added {len(transactions)} transactions to the database.")


if __name__ == "__main__":
    seed_database()
