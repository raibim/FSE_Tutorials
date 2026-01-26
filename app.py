from datetime import datetime
from decimal import Decimal

from helpers.transactions import Transaction, Category, calculate_financial_summary
from data.database import get_session
from helpers.analysis import generate_financial_charts, generate_text_report



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
        display_transactions_by_category("Income")
        display_transactions_by_category("Expense")
        generate_financial_charts()
        print(generate_text_report())


# This function should group and display transactions by category, so we can see like Income - 3 transactions, Expense - 2 transactions, etc.
def display_transactions_by_category(category_name: str):
    session = get_session()
    try:
        transactions = session.query(Transaction).filter_by(category=category_name).all()
        if not transactions:
            print(f"No transactions found in category '{category_name}'.")
            return
        print(f"\nTransactions in category '{category_name}':")
        for t in transactions:
            print(t)
    finally:
        session.close()


if __name__ == "__main__":
    main()
