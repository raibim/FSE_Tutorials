import os
import matplotlib

from data.database import get_session
from helpers.transactions import Category, Transaction

matplotlib.use("Agg")  # Fixes potential backend issues
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import func, cast, Float

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "..", "static")


def generate_financial_charts():
    """Generates two pie charts: one for Expenses and one for Income."""
    session = get_session()
    charts = {}

    try:
        # 1. Query for Expenses (Amount < 0)
        expense_results = (
            session.query(
                Transaction.category,  # Grouping by the string 'category' for more detail
                func.abs(cast(func.sum(Transaction.amount), Float)).label("total"),
            )
            .filter(Transaction.amount < 0)
            .group_by(Transaction.category)
            .all()
        )

        # 2. Query for Income (Amount > 0)
        income_results = (
            session.query(
                Transaction.category,
                cast(func.sum(Transaction.amount), Float).label("total"),
            )
            .filter(Transaction.amount > 0)
            .group_by(Transaction.category)
            .all()
        )
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
        print(f"No data found for {title}.")
        return None

    df = pd.DataFrame(data, columns=["label", "total"])
    plt.figure(figsize=(8, 8))
    plt.pie(df["total"], labels=df["label"].tolist(), autopct="%1.1f%%", startangle=140)
    plt.title(title)

    path = os.path.join(STATIC_DIR, filename)
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")
    return path


def create_unified_dataframe() -> pd.DataFrame:
    """Fetches all transactions and returns a unified DataFrame."""
    session = get_session()
    try:
        results = session.query(
            Transaction.date,
            Transaction.description,
            Transaction.amount,
            Transaction.category,
        ).all()
        df = pd.DataFrame(results, columns=["date", "description", "amount", "category"])
        return df
    finally:
        session.close()



#TODO Complete the function below
def generate_text_report():
    """Generates a text-based financial report."""
    df = create_unified_dataframe()
    # Ensure amount is numeric and date is datetime
    df['amount'] = pd.to_numeric(df['amount'])
    df['date'] = pd.to_datetime(df['date'])

    #TODO Get an object called expenses by using df[df['amount'] < 0], and income by using df[df['amount'] > 0]

    # Once you have those two objects, complete the following calculations, uncomment them!
    # total_spent = abs(expenses['amount'].sum())
    # total_earned = income['amount'].sum()

    # 2. Average Spend! Calculate how much we have spent in total, and divide it by the number of days in the period.
    # NOTE: I have given you the code to calculate days_in_period, you just need to calculate daily_burn.
    # HINT: For the data we have, the daily burn should be about R 615.41
    #Uncomment the lines below once you have the total spent and earned variables
    # days_in_period = (df['date'].max() - df['date'].min()).days or 1
    # daily_burn = ?

    # 3. Category Breakdown by percentage for the category 'Dining Out'
    # dining_out = abs(df[df['category'] == 'Dining Out']['amount'].sum())
    #NOTE: Dining out percentage is how much we spent on dining out as a percentage of our total spending.
    # HINT: For the data we have, the dining out percentage should be about 1.9%
    # dining_pct = ?

    # 4. Essential Coverage Ratio: How well does your income from 'Job' cover essential expenses like 'Housing' and 'Utilities'?

    # This would be your job income over your essential expenses, if you have any essentials.
    #NOTE: I have given you the code to calculate essentials, you just need to calculate job_income and coverage_ratio.
    # essentials = abs(df[df['category'].isin(['Housing', 'Utilities'])]['amount'].sum())

    # job_income = ?
    # coverage_ratio = ?

    # Output Report
    #NOTE: Please uncomment the return statement below once you have all the variables calculated and properly assigned.
    # return {
    #     "Daily Burn Rate": f"R {daily_burn:.2f}",
    #     "Dining Out %": f"{dining_pct:.1f}%",
    #     "Essential Coverage": "Healthy" if coverage_ratio >= 2 else "Tight",
    #     "Net Savings": f"R {total_earned - total_spent:.2f}"
    # }
