import pytest
from decimal import Decimal
from unittest.mock import patch

from app import app
from helpers.transactions import Transaction


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_text_report():
    """Mock data matching the structure returned by generate_text_report()."""
    return {
        "Daily Burn Rate": "R 615.41",
        "Dining Out %": "1.9%",
        "Essential Coverage": "Healthy",
        "Net Savings": "R 56006.25"
    }


def test_financial_summary_endpoint(client, mock_text_report):
    """Test that /api/financial_summary returns the correct text report."""
    with patch('app.generate_text_report', return_value=mock_text_report):
        response = client.get('/api/financial_summary')
        
        assert response.status_code == 200
        assert response.is_json
        
        data = response.get_json()
        assert "Daily Burn Rate" in data
        assert "Dining Out %" in data
        assert "Essential Coverage" in data
        assert "Net Savings" in data
        
        assert data["Daily Burn Rate"] == "R 615.41"
        assert data["Dining Out %"] == "1.9%"
        assert data["Essential Coverage"] == "Healthy"
        assert data["Net Savings"] == "R 56006.25"


def test_financial_summary_returns_json(client, mock_text_report):
    """Test that the endpoint returns valid JSON with correct content type."""
    with patch('app.generate_text_report', return_value=mock_text_report):
        response = client.get('/api/financial_summary')
        
        assert response.content_type == 'application/json'
        assert response.status_code == 200


def test_financial_charts_endpoint(client):
    """Test that /api/financial_charts returns chart paths."""
    mock_charts = {
        "expenses": "/path/to/expenses_pie.png",
        "income": "/path/to/income_pie.png"
    }
    
    with patch('app.generate_financial_charts', return_value=mock_charts):
        response = client.get('/api/financial_charts')
        
        assert response.status_code == 200
        assert response.is_json
        
        data = response.get_json()
        assert "expenses" in data
        assert "income" in data
        assert data["expenses"] == "/static/expenses_pie.png"
        assert data["income"] == "/static/income_pie.png"


def test_transactions_by_category_endpoint(client):
    """Test that /api/transactions returns filtered transactions by category."""
    mock_transactions = [
        Transaction(
            id=1,
            date="2026-01-23T14:36:28",
            description="Pick n Pay Groceries",
            amount=Decimal("-1250.50"),
            category="Groceries"
        ),
        Transaction(
            id=2,
            date="2025-12-17T14:36:28",
            description="Checkers Groceries",
            amount=Decimal("-1100.25"),
            category="Groceries"
        )
    ]
    
    with patch('app.get_session') as mock_get_session:
        mock_session = mock_get_session.return_value
        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter_by.return_value
        mock_filter.all.return_value = mock_transactions
        
        response = client.get('/api/transactions?category=Groceries')
        
        assert response.status_code == 200
        assert response.is_json
        
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["category"] == "Groceries"
        assert data[0]["description"] == "Pick n Pay Groceries"
        assert data[1]["description"] == "Checkers Groceries"


def test_transactions_endpoint_missing_category(client):
    """Test that /api/transactions handles missing category parameter."""
    response = client.get('/api/transactions')
    
    # Should still return 200 but with empty list or error message
    assert response.status_code == 200
    assert response.is_json
