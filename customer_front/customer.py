import os

from flask import Blueprint, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Blueprint keeps the demo UI isolated but easy to register in app.py
customer_bp = Blueprint(
    "customer",
    __name__,
    static_folder=BASE_DIR,
    template_folder=BASE_DIR,
)


@customer_bp.route("/")
def serve_dashboard():
    return send_from_directory(BASE_DIR, "customer.html")


@customer_bp.route("/style.css")
def serve_styles():
    return send_from_directory(BASE_DIR, "customer.css")
