import os
from celery import Celery
from loguru import logger
from data.database import get_session
from helpers.transactions import Transaction
from helpers.analysis import generate_financial_charts
from helpers.config import Config
import time

# Configure logger for Celery workers to write to the same log file as Flask app
logger.remove()
logger.add("logs/app.log", format="{message}")

# Initialize Celery app
celery = Celery(
    "fse_app",
    broker=Config.get_celery_broker_url(),
    backend=Config.get_celery_result_backend(),
)


def charts_exist() -> bool:
    """Check if chart files already exist in the static directory."""
    STATIC_DIR = Config.get_static_dir()
    expense_chart = os.path.join(STATIC_DIR, "expenses_pie.png")
    income_chart = os.path.join(STATIC_DIR, "income_pie.png")
    return os.path.exists(expense_chart) and os.path.exists(income_chart)


# NOTE: We care about this result, we will return it to the caller since it contains paths to the generated charts
# This is why we use Redis! It acts as our result backend since we put the paths there.
# Notably, redis is ALSO used as the broker to send tasks to workers.
@celery.task(name="generate_charts_task")
def generate_charts_task():
    """Celery task to generate financial charts asynchronously."""
    # Check if charts already exist, if so we can skip regeneration
    if charts_exist():
        STATIC_DIR = Config.get_static_dir()
        return {
            "expenses": os.path.join(STATIC_DIR, "expenses_pie.png"),
            "income": os.path.join(STATIC_DIR, "income_pie.png"),
        }
    charts = generate_financial_charts()
    # NOTE: Delay added to simulate long processing time for testing
    time.sleep(5)  # Sleep for 5 seconds
    web_paths = {}
    for key, path in charts.items():
        if path:
            web_paths[key] = (
                f"{os.path.join(Config.get_static_dir(), os.path.basename(path))}"
            )
    return web_paths



# TODO: Implement the function below to log a transaction
# Remember to get the session, query the transaction by ID, and then call the log_transaction_audit helper function
# If the transaction is not found, print an error message: "Transaction with ID {transaction_id} not found for audit logging."
@celery.task(name="log_transaction_audit_task")
def log_transaction_audit_task(transaction_id: int):
    """Celery task to log transaction audit information."""
    session = get_session()
    try:
        transaction = session.query(Transaction).filter_by(id=transaction_id).first()
        if transaction:
            log_transaction_audit(transaction)
        else:
            logger.error(f"Transaction with ID {transaction_id} not found for audit logging.")
    finally:
        session.close()


def log_transaction_audit(transaction: Transaction):
    """Helper function to log transaction audit information."""
    logger.info(f"Audit Log - Transaction ID: {transaction.id}, Date: {transaction.date}, Description: {transaction.description}, Amount: {transaction.amount}, Category: {transaction.category_ref.name if transaction.category_ref else 'None'}")
