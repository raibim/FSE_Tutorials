import os
from datetime import datetime
from decimal import Decimal

from flask import Flask, jsonify, request

from customer_front.customer import customer_bp
from data.database import get_session
from helpers.analysis import generate_financial_charts, generate_text_report
from helpers.transactions import Category, Transaction


app = Flask(__name__)
app.register_blueprint(customer_bp, url_prefix="/")

#TODO Complete the API endpoint below
#NOTE You should use jsonify to return the report from generate_text_report()
@app.route("/api/financial_summary", methods=["GET"])
def api_financial_summary():
    """API endpoint to get the student-facing text report."""
    return ""


#TODO Complete the API endpoint below to return transactions for a specific category
#NOTE Accept a query parameter 'category' (e.g., /api/transactions?category=Groceries)
#NOTE Query the database for transactions matching that category
#NOTE Return a JSON list of transaction dictionaries with keys: id, date, description, amount, category
#HINT You can use request.args.get('category') to get the query parameter
@app.route("/api/transactions", methods=["GET"])
def api_transactions_by_category():
    """API endpoint to get transactions filtered by category."""
    return ""


@app.route("/api/financial_charts", methods=["GET"])
def api_financial_charts():
    """Optionally generate charts and return web-friendly paths."""
    charts = generate_financial_charts()
    web_paths = {}
    for key, path in charts.items():
        if path:
            web_paths[key] = f"/static/{os.path.basename(path)}"
    return jsonify(web_paths)


if __name__ == "__main__":
    app.run(debug=True)
