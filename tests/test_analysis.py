import pytest
from unittest.mock import patch
import pandas as pd
from helpers.analysis import generate_text_report

@pytest.fixture
def mock_dataframe():
    """Returns a DataFrame populated with 2 months of financial data."""
    data = [
        {"date": "2026-01-25T14:36:28", "description": "Monthly Salary", "amount": 35000.00, "category": "Job"},
        {"date": "2026-01-23T14:36:28", "description": "Pick n Pay Groceries", "amount": -1250.50, "category": "Groceries"},
        {"date": "2026-01-21T14:36:28", "description": "Rent Payment", "amount": -12000.00, "category": "Housing"},
        {"date": "2026-01-16T14:36:28", "description": "Freelance Project: Web Design", "amount": 4500.00, "category": "Freelance"},
        {"date": "2026-01-14T14:36:28", "description": "Electricity/Water Bill", "amount": -1850.00, "category": "Utilities"},
        {"date": "2026-01-11T14:36:28", "description": "Netflix Subscription", "amount": -199.00, "category": "Entertainment"},
        {"date": "2026-01-08T14:36:28", "description": "Petrol Station", "amount": -950.00, "category": "Transport"},
        {"date": "2026-01-04T14:36:28", "description": "Dinner with Friends", "amount": -650.00, "category": "Dining Out"},
        {"date": "2025-12-30T14:36:28", "description": "Year-End Bonus", "amount": 15000.00, "category": "Bonus"},
        {"date": "2025-12-29T14:36:28", "description": "Monthly Salary", "amount": 35000.00, "category": "Job"},
        {"date": "2025-12-25T14:36:28", "description": "Holiday Gift Shopping", "amount": -4200.00, "category": "Shopping"},
        {"date": "2025-12-22T14:36:28", "description": "Rent Payment", "amount": -12000.00, "category": "Housing"},
        {"date": "2025-12-17T14:36:28", "description": "Checkers Groceries", "amount": -1100.25, "category": "Groceries"},
        {"date": "2025-12-12T14:36:28", "description": "Internet Fiber Line", "amount": -899.00, "category": "Utilities"},
        {"date": "2025-12-07T14:36:28", "description": "Coffee Shop", "amount": -45.00, "category": "Dining Out"},
        {"date": "2025-12-02T14:36:28", "description": "Gym Membership", "amount": -550.00, "category": "Health"},
        {"date": "2025-11-28T14:36:28", "description": "Freelance Project: Logo", "amount": 2200.00, "category": "Freelance"}
    ]
    
    df = pd.DataFrame(data)
    
    # Crucial for the tutorial: Ensure types are correct immediately
    df['date'] = pd.to_datetime(df['date'])
    # Using float here for simple pandas math, or Decimal if you want to be strict
    df['amount'] = df['amount'].astype(float) 
    
    return df


@pytest.fixture
def expected_output():
    """Expected output from generate_text_report."""
    return {
        'Daily Burn Rate': 'R 615.41',
        'Dining Out %': '1.9%',
        'Essential Coverage': 'Healthy',
        'Net Savings': 'R 56006.25'
    }


@patch('helpers.analysis.create_unified_dataframe')
def test_generate_text_report(mock_create_df, mock_dataframe, expected_output):
    """Test generate_text_report returns expected output format."""
    mock_create_df.return_value = mock_dataframe
    
    result = generate_text_report()
    
    assert isinstance(result, dict)
    assert set(result.keys()) == set(expected_output.keys())
    assert result['Daily Burn Rate'] == expected_output['Daily Burn Rate']
    assert result['Dining Out %'] == expected_output['Dining Out %']
    assert result['Essential Coverage'] == expected_output['Essential Coverage']
    assert result['Net Savings'] == expected_output['Net Savings']