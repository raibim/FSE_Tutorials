from decimal import Decimal
import os
from loguru import logger
import matplotlib

from data.database import get_session
from helpers.transactions import Category, Transaction

matplotlib.use("Agg")  # Fixes potential backend issues
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import func, cast, Float, select

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "..", "static")


def generate_financial_charts():
    """Generates two pie charts: one for Expenses and one for Income."""
    session = get_session()
    charts = {}

    try:
        # 1. We can fetch all the categories since they are linked to transactions
        stmt = select(Category).join(Transaction).group_by(Category.id)
        categories = session.execute(stmt).scalars().all()
        if not categories:
            logger.info("No categories with transactions found for chart generation.")
            return charts
        # Now we can filter our categories into expenses and income
        # 1. Get the sum of negative amounts (expenses) grouped by category
        expense_results = []
        income_results = []
        for category in categories:
            total_expense = sum(
                Decimal(str(t.amount))
                for t in category.transactions
                if Decimal(str(t.amount)) < 0
            )
            total_income = sum(
                Decimal(str(t.amount))
                for t in category.transactions
                if Decimal(str(t.amount)) > 0
            )
            if total_expense < 0:
                expense_results.append((category.name, float(abs(total_expense))))
            if total_income > 0:
                income_results.append((category.name, float(total_income)))

        charts["expenses"] = create_pie(
            expense_results, "Expenses by Category", "expenses_pie.png"
        )
        charts["income"] = create_pie(
            income_results, "Income by Category", "income_pie.png"
        )
        return charts
    finally:
        session.close()


def create_pie(data, title, filename):
    if not data:
        logger.warning(f"No data available to create pie chart: {title}")
        return None

    df = pd.DataFrame(data, columns=["label", "total"])
    plt.figure(figsize=(8, 8))
    plt.pie(df["total"], labels=df["label"].tolist(), autopct="%1.1f%%", startangle=140)
    plt.title(title)

    path = os.path.join(STATIC_DIR, filename)
    plt.savefig(path)
    plt.close()
    logger.success(f"Saved: {path}")
    return path


def create_unified_dataframe() -> pd.DataFrame:
    """Fetches all transactions and returns a unified DataFrame."""
    session = get_session()
    try:
        stmt = select(Category).join(Transaction).group_by(Category.id)
        categories = session.execute(stmt).scalars().all()

        if not categories:
            logger.info("No categories with transactions found for DataFrame creation.")
            return pd.DataFrame(columns=["date", "description", "amount", "category"])

        # Now we have all categories with their transactions, we can build the DataFrame
        results = []
        for category in categories:
            for t in category.transactions:
                results.append((t.date, t.description, t.amount, category.name))
        df = pd.DataFrame(
            results, columns=["date", "description", "amount", "category"]
        )
        return df
    finally:
        session.close()


# TODO Complete the function below
def generate_text_report() -> dict:
    """Generates a text-based financial report."""
    df = create_unified_dataframe()
    if df.empty:
        return {
            "Daily Burn Rate": "R 0.00",
            "Dining Out %": "0.0%",
            "Essential Coverage": "No data",
            "Net Savings": "R 0.00",
        }
    # Ensure amount is numeric and date is datetime
    df["amount"] = pd.to_numeric(df["amount"])
    df["date"] = pd.to_datetime(df["date"])

    # TODO Get an object called expenses that contains only the expenses (negative amounts)
    expenses = df[df["amount"] < 0]  # this returns columns where the amount is negative
    # TODO Get an object called income that contains only the income (positive amounts)
    income = df[df["amount"] > 0]

    # Once you have those two objects, complete the following calculations, uncomment them!
    total_spent = abs(expenses["amount"].sum())
    total_earned = income["amount"].sum()

    # 2. Average Spend! Calculate how much we have spent in total, and divide it by the number of days in the period.
    # NOTE: I have given you the code to calculate days_in_period, you just need to calculate daily_burn.
    # HINT: For the data we have, the daily burn should be about R 615.41
    # Uncomment the lines below once you have the total spent and earned variables
    days_in_period = (
        df["date"].max() - df["date"].min()
    ).days or 1  # this looks at data column in dataframe and finds atest date and then finds the oldest date and subtracts
    daily_burn = total_spent / days_in_period

    # 3. Category Breakdown by percentage for the category 'Entertainment''
    # NOTE: Entertainment percentage is how much we spent on entertainment as a percentage of our total spending.
    entertainment = abs(
        expenses[expenses["category"] == "Entertainment"]["amount"].sum()
    )
    entertainment_pct = (entertainment / total_spent) * 100 if total_spent > 0 else 0

    # 4. Essential Coverage Ratio: How well does your income from 'Job' cover essential expenses like 'Housing' and 'Utilities'?
    # NOTE: I have given you the code to calculate essentials, you just need to calculate job_income and coverage_ratio.

    essentials = abs(df[df["category"].isin(["Housing", "Utilities"])]["amount"].sum())
    job_income = income[income["category"] == "Job"]["amount"].sum()
    coverage_ratio = job_income / essentials if essentials > 0 else float("inf")

    # Output Report
    # NOTE: Please uncomment the return statement below once you have all the variables calculated and properly assigned.
    return {
        "Daily Burn Rate": f"R {daily_burn:.2f}",
        "Entertainment %": f"{entertainment_pct:.1f}%",
        "Essential Coverage": "Healthy" if coverage_ratio >= 2 else "Tight",
        "Net Savings": f"R {total_earned - total_spent:.2f}",
    }


def display_transactions_by_category(category_name: str):
    session = get_session()
    try:
        stmt = select(Category).where(Category.name == category_name)
        category = session.execute(stmt).scalars().first()
        if not category or not category.transactions:
            logger.info(f"No transactions found for category '{category_name}'.")
            return
        logger.info(f"Transactions for category '{category_name}':")
        for t in category.transactions:
            logger.info(t)
    finally:
        session.close()
