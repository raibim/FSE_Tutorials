import os
from datetime import datetime
from decimal import Decimal

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from customer_front.customer import customer_bp
from data.database import get_session
from helpers.analysis import generate_financial_charts, generate_text_report
from helpers.transactions import Category, Transaction
from helpers.config import Config



app = Flask(__name__)
app.secret_key = Config.get_secret_key()
app.register_blueprint(customer_bp, url_prefix="/customer")


@app.route("/")
def dashboard():
    """Main dashboard with Jinja2 template."""
    session = get_session()
    try:
        # Get all transactions
        transactions = session.query(Transaction).order_by(Transaction.date.desc()).all()
        
        # Get financial report
        report = generate_text_report()
        
        # Generate charts and get paths
        charts = generate_financial_charts()
        chart_paths = {}
        for key, path in charts.items():
            if path:
                chart_paths[key] = f"/static/{os.path.basename(path)}"
        
        largest_expense = session.query(Transaction).filter(Transaction.amount < 0).order_by(Transaction.amount).first()
        avg_transaction = session.query(Transaction).with_entities(
            (Transaction.amount).label('amount')
        ).all()
        if avg_transaction:
            avg_transaction = sum([t.amount for t in avg_transaction]) / len(avg_transaction)
        else:
            avg_transaction = 0
        
        return render_template(
            'dashboard.html',
            transactions=transactions,
            report=report,
            chart_paths=chart_paths,
            largest_expense=largest_expense,
            avg_transaction=avg_transaction
        )
    finally:
        session.close()


@app.route("/transaction/add", methods=["POST"])
def add_transaction():
    """Handle adding a new transaction."""
    session = get_session()
    try:
        # Extract form data
        date_str = request.form.get('date')
        description = request.form.get('description')
        amount = Decimal(request.form.get('amount', '0'))
        category = request.form.get('category')
        transaction_type = request.form.get('transaction_type')
        
        # Validate required fields
        if not date_str:
            raise ValueError("Date is required")
        
        # Make amount negative if it's an expense
        if transaction_type == 'expense':
            amount = -abs(amount)
        else:
            amount = abs(amount)
        
        # Parse date - handle both datetime-local format and ISO format with microseconds
        try:
            # Try datetime-local format first (YYYY-MM-DDTHH:MM)
            parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                # Try with seconds (YYYY-MM-DDTHH:MM:SS)
                parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                # Try with microseconds (YYYY-MM-DDTHH:MM:SS.ffffff)
                parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        
        # Create new transaction
        new_transaction = Transaction(
            date=parsed_date.isoformat(),
            description=description,
            amount=amount,
            category=category
        )
        
        session.add(new_transaction)
        session.commit()
        
        flash('Transaction added successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error adding transaction: {str(e)}', 'error')
    finally:
        session.close()
    
    return redirect(url_for('dashboard'))


@app.route("/api/financial_summary", methods=["GET"])
def api_financial_summary():
    """API endpoint to get the student-facing text report."""
    return jsonify(generate_text_report())


@app.route("/api/transactions", methods=["GET"])
def api_transactions_by_category():
    """API endpoint to get transactions filtered by category."""
    category = request.args.get("category")
    if not category:
        return jsonify([])  # Return empty list if no category provided
    session = get_session()
    try:
        transactions = session.query(Transaction).filter_by(category=category).all()
        result = [
            {
                "id": t.id,
                "date": t.date,
                "description": t.description,
                "amount": t.amount,
                "category": t.category,
            }
            for t in transactions
        ]
        return jsonify(result)
    finally:
        session.close()


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
    app.run(host="0.0.0.0", port=5000, debug=Config.get_debug_mode())
