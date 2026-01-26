# Tutorial 7: Building a RESTful API with Flask

In this tutorial, we transform our application from a command-line tool into a **Web API** using **Flask**. You will implement API endpoints that serve financial data to a front-end dashboard, learning the fundamentals of modern web architecture in the process.

### Learning Objectives

* Understand what an **API** is and why it separates backend logic from user interfaces.
* Learn how to use **Flask** to build RESTful endpoints.
* Implement routes that return JSON responses.
* Handle query parameters to filter data dynamically.
* Test your API endpoints using automated tests.

---

## What is Flask?

**Flask** is a lightweight Python web framework that makes it easy to build web applications and APIs. Think of it as a tool that:
- Listens for HTTP requests (like when a user visits a URL)
- Runs your Python code in response
- Sends back data (usually as JSON) or HTML pages

In our case, we're using Flask to build a **REST API**—a set of URLs that return data instead of web pages. This allows any client (web browser, mobile app, or another program) to request financial data from our application.

## What is an API?

An **API** (Application Programming Interface) is like a waiter in a restaurant:
- The kitchen (your backend/database) has all the data
- The customer (front-end/user) wants that data
- The waiter (API) takes requests from the customer and brings back exactly what they asked for

Instead of building everything into one monolithic program, modern applications are split into:
1. **Backend API** (what you're building in `app.py`) - handles data, calculations, and business logic
2. **Frontend** (the `customer_front/` folder) - displays data in a user-friendly way

This separation means you could build multiple frontends (web, mobile, desktop) that all use the same API!

---

## Understanding the customer_front Folder

The `customer_front/` folder contains a minimal web dashboard that **consumes** your API. It's a simple HTML/CSS/JavaScript page that:
- Fetches data from your API endpoints using HTTP requests
- Displays financial summaries in styled cards
- Shows spending and income charts

This demonstrates the power of APIs: the frontend doesn't know *how* you calculate burn rates or query the database—it just asks the API and displays the results.

---

### Step 1: Check Out the tut-7 Branch

```bash
git checkout tut-7
```

### Step 2: Review the Application Structure

Your `app.py` now uses Flask to define **routes**—URLs that respond to HTTP requests:

```python
@app.route("/api/financial_summary", methods=["GET"])
def api_financial_summary():
    # Your code will return JSON data here
    return ""
```

Each route is like a function that runs when someone visits that URL. The `@app.route()` decorator tells Flask which URL should trigger which function.

---

### Step 3: Complete the TODO Endpoints

You have **two endpoints** to implement in `app.py`:

#### Endpoint 1: `/api/financial_summary`

**What it does**: Returns a summary report with Daily Burn Rate, Dining Out %, Essential Coverage, and Net Savings.

**Your task**:
1. Call `generate_text_report()` (already imported from `helpers.analysis`)
2. Use `jsonify()` to convert the dictionary to a JSON response
3. Return the result


#### Endpoint 2: `/api/transactions`

**What it does**: Returns all transactions for a specific category (e.g., "Groceries").

**Your task**:
1. Get the `category` query parameter using `request.args.get('category')`
2. Query the database for transactions matching that category
3. Convert Transaction objects to dictionaries
4. Return a JSON list

**Hints**:
- Use `get_session()` to get a database session
- Query: `session.query(Transaction).filter_by(category=category_name).all()`
- Convert each transaction to a dict: `{"id": t.id, "date": t.date, "description": t.description, "amount": str(t.amount), "category": t.category}`
- Don't forget to close the session in a `finally` block!

---

### Step 4: Run the Flask Application

Start your API server:

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

Your API is now live! Open your browser and visit:
- **http://localhost:5000/** - View the customer dashboard
- **http://localhost:5000/api/financial_summary** - See the JSON summary
- **http://localhost:5000/api/transactions?category=Groceries** - See filtered transactions

---

### Step 5: Test Your API Endpoints

I've provided comprehensive tests in `tests/test_flask_api.py`. Run them to verify your implementation:

```bash
pytest tests/test_flask_api.py -v
```

These tests verify:
- Your endpoints return valid JSON
- The data structure is correct
- Query parameters work properly
- Edge cases are handled (e.g., missing category parameter)

**All tests should pass** when you've correctly implemented both endpoints.

---

### Step 6: Interact with the Dashboard

With the Flask server running, open http://localhost:5000 in your browser. You should see:

1. **Financial Summary Cards** - Click "Refresh Summary" to fetch data from `/api/financial_summary`
2. **Charts Section** - Click "Load Charts" to fetch and display your spending/income pie charts

The dashboard uses JavaScript to make HTTP requests to your API and dynamically update the page. This is how modern web applications work!

---

### Step 7: Run All Tests

Ensure your entire application still works:

```bash
pytest tests/ -v
```

All tests across all modules should pass.

---

### Step 8: Commit Your Work

1. **Stage your changes**: Use your editor's Source Control tab to stage `app.py`
2. **Commit**:
```bash
git commit -m "Completed Tutorial 7: Built Flask REST API with financial endpoints"
```

---

## Summary

* **Flask** is a lightweight framework for building web applications and APIs in Python.
* **REST APIs** separate backend logic from frontend presentation, enabling flexible architectures.
* **Routes** (`@app.route()`) define URL endpoints that execute Python functions.
* **Query parameters** allow clients to filter or customize API responses.
* **JSON** is the standard format for API data exchange—use `jsonify()` to convert Python dicts to JSON.
* The **customer_front/** folder represents a client application that consumes your API, demonstrating the separation of concerns.

You've now built a working web API that can power any frontend—web, mobile, or desktop. This architecture is the foundation of modern software development!

---

## Key Concepts Recap

### API Architecture
```
┌─────────────┐      HTTP GET /api/financial_summary      ┌──────────┐
│   Frontend  │ ──────────────────────────────────────► │  Flask   │
│  (Browser)  │                                           │   API    │
│             │ ◄────────────── JSON Response ─────────── │          │
└─────────────┘      {"Daily Burn Rate": "R 615.41"}     └──────────┘
                                                                │
                                                                ▼
                                                          ┌──────────┐
                                                          │ Database │
                                                          └──────────┘
```

### What You Built
- RESTful API endpoints that return financial data
- Query parameter handling for filtered results
- JSON serialization of database objects
- Separation of backend (API) and frontend (dashboard)
- Automated tests to verify API behavior

Congratulations on building your first web API! 🎉
