from loguru import logger

from transactions import Transaction, Category, calculate_financial_summary
from database import get_session
from sqlalchemy import select
from decimal import Decimal



def main():
    logger.add("logs/app.log", rotation="1 MB")
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
        logger.error(
            f"You may need to seed the database first, run 'python seed.py' and try again.\n\n"
        )
        raise e

    finally:
        session.close()
        # TODO: Once you have added the Entertainment category and sample  expenses, uncomment the lines below to display them!
        # display_transactions_by_category("Job")
        # display_transactions_by_category("Entertainment")


# TODO: Add the entertainment category, if it does not already exist
# NOTE: This means checking if a category with that name exists first
def add_entertainment_category():
    session = get_session()
    try:
         #check if entertainment exists
       category_exists=session.query(Category).filter_by(name="Entertainment").first()
       if category_exists:
           return
       session.add(Category(name="Entertainment"))
       session.commit()
    finally:
        session.close()


# TODO: Add sample entertainment expenses
# NOTE: Fetch the Entertainment category first, then add two sample expenses linked to that category
def add_entertainment_expenses():
    session = get_session()
    try:
     #step 1:check entertainment category exists
       entertainment_category = session.query(Category).filter_by(name="Entertainment").first()
     #step 2: if it does exists, add two sample expenses with negative amounts under the entertainment category
       if entertainment_category:
            expense1 = Transaction(
                date="2024-03-01",
                description="Movie Tickets",
                amount=Decimal("-150.00"),
                category_ref=entertainment_category,
            )
            expense2 = Transaction(
                date="2024-03-05",
                description="Concert",
                amount=Decimal("-300.00"),
                category_ref=entertainment_category,
            )
            session.add_all([expense1, expense2])
            session.commit()


     #step 3: add the expenses to the database and commit

       
    finally:
        session.close()


# TODO: Display all transactions for a given category name
def display_transactions_by_category(category_name: str):
    session = get_session()
    try:
        #fetch category and print the result
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            logger
        transactions = session.query(Transaction).filter_by(category_id=category.id).all()
        print
        for transaction in transactions:
            print(transaction)
    except Exception as e:
        logger.error(
            f"Error displaying transactions for category '{category_name}': {e}"
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
