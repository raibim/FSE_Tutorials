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



def generate_text_report():
    """Generates a text-based financial report."""
    df = create_unified_dataframe()
    # Ensure amount is numeric and date is datetime
    df['amount'] = pd.to_numeric(df['amount'])
    df['date'] = pd.to_datetime(df['date'])

    expenses = df[df['amount'] < 0]
    income = df[df['amount'] > 0]
    
    total_spent = abs(expenses['amount'].sum())
    total_earned = income['amount'].sum()

    days_in_period = (df['date'].max() - df['date'].min()).days or 1
    daily_burn = total_spent / days_in_period

    dining_out = abs(df[df['category'] == 'Dining Out']['amount'].sum())
    dining_pct = (dining_out / total_spent) * 100 if total_spent > 0 else 0

    essentials = abs(df[df['category'].isin(['Housing', 'Utilities'])]['amount'].sum())
    job_income = income[income['category'] == 'Job']['amount'].sum()
    coverage_ratio = job_income / essentials if essentials > 0 else 0

    # Output Report
    return {
        "Daily Burn Rate": f"R {daily_burn:.2f}",
        "Dining Out %": f"{dining_pct:.1f}%",
        "Essential Coverage": "Healthy" if coverage_ratio >= 2 else "Tight",
        "Net Savings": f"R {total_earned - total_spent:.2f}"
    }
