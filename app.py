from datetime import datetime
from decimal import Decimal
from sqlite3 import OperationalError

from helpers.transactions import Transaction, Category, calculate_financial_summary
from data.database import get_session


def main():
    # Initialize database and create tables
    # Get a session
    session = get_session()

    try:
        # Ensure transaction table exists by querying it
        session.query(Transaction).first()

        # Query all transactions from the database
        all_transactions = session.query(Transaction).all()

        # Calculate and display summary
        summary = calculate_financial_summary(all_transactions)
        print("Financial Summary:")
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    except Exception as e:
        print(f"You may need to seed the database first, run 'python seed.py' and try again.\n\n")
        raise e

    finally:
        session.close()
        #TODO: Once you have added the expense category and sample expenses, uncomment the lines below to display them!
        # display_transactions_by_category("Income")
        # display_transactions_by_category("Expense")


#TODO: Add the expense category if it does not exist, check if it exists first like we do above!
def add_expense_category():
    session = get_session()
    try:
        expense_category = session.query(Category).filter_by(name="Expense").first()

        if not expense_category:
            expense_category = Category(name="Expense")
            session.add(expense_category)
            session.commit()  # Commit now so the ID is available
            print("Created new 'Expense' category.")
        else:
            print("Using existing 'Expense' category.")
    finally:
        session.close()

#TODO: Add sample expenses if they do not exist
def add_expenses():
    session = get_session()
    try:
        existing_expenses = session.query(Transaction).filter(Transaction.amount < 0).first()
        if not existing_expenses:
            expense_category = session.query(Category).filter_by(name="Expense").first()
            if not expense_category:
                print("Expense category does not exist. Please run add_expense_category() first.")
                return

            expenses = [
                Transaction(
                    date=datetime.now().isoformat(),
                    description="Groceries",
                    amount=Decimal("-600"),
                    category="Food",
                    category_ref=expense_category,
                ),
                Transaction(
                    date=datetime.now().isoformat(),
                    description="Utilities",
                    amount=Decimal("-300"),
                    category="Bills",
                    category_ref=expense_category,
                ),
            ]

            for expense in expenses:
                session.add(expense)
            session.commit()
            print("Created and added sample expenses to the database.")
        else:
            print("Expenses already exist in the database. No new expenses added.")
    finally:
        session.close()

# This function should group and display transactions by category, so we can see like Income - 3 transactions, Expense - 2 transactions, etc.
def display_transactions_by_category(category_name: str):
    session = get_session()
    try:
        transactions = session.query(Transaction).filter_by(category=category_name).all()
        print(f"\nTransactions in category '{category_name}':")
        for t in transactions:
            print(t)
    finally:
        session.close()


if __name__ == "__main__":
    main()
