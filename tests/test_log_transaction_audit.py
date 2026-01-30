import os
import pytest
from unittest.mock import patch
from io import StringIO
from data.database import get_session
from helpers.transactions import Transaction
from tasks import log_transaction_audit_task


@pytest.fixture
def test_transaction():
    """Create a test transaction in the database."""
    session = get_session()
    try:
        transaction = Transaction(
            date="2026-01-30T10:00:00",
            description="Test Transaction",
            amount=100.50,
            category="Test",
        )
        session.add(transaction)
        session.commit()
        transaction_id = transaction.id
        return transaction_id
    finally:
        session.close()


@pytest.fixture
def cleanup_log_file():
    """Remove the log file before and after each test."""
    log_file = "transaction_audit.log"
    if os.path.exists(log_file):
        os.remove(log_file)
    yield
    if os.path.exists(log_file):
        os.remove(log_file)


def test_log_transaction_with_valid_id(test_transaction, cleanup_log_file):
    """Test that log_transaction_audit_task writes log file with valid transaction ID."""
    transaction_id = test_transaction

    # Run the task
    log_transaction_audit_task(transaction_id)

    # Check that log file was created
    assert os.path.exists("transaction_audit.log"), "Log file should be created"

    # Check that log file contains transaction information
    with open("transaction_audit.log", "r") as log_file:
        log_content = log_file.read()
        assert f"Transaction ID: {transaction_id}" in log_content
        assert "Test Transaction" in log_content
        assert "100.5" in log_content
        assert "Test" in log_content


def test_log_transaction_with_invalid_id(cleanup_log_file, capsys):
    """Test that log_transaction_audit_task prints error with invalid transaction ID."""
    invalid_id = 999999

    # Run the task with an invalid ID
    log_transaction_audit_task(invalid_id)

    # Capture printed output
    captured = capsys.readouterr()

    # Check that error message was printed
    assert (
        f"Transaction with ID {invalid_id} not found for audit logging." in captured.out
    )

    # Check that no log file was created (or if it exists, it shouldn't have the invalid ID)
    if os.path.exists("transaction_audit.log"):
        with open("transaction_audit.log", "r") as log_file:
            log_content = log_file.read()
            assert f"Transaction ID: {invalid_id}" not in log_content
