# Tutorial 2

## Building the Transactions Module

In this tutorial, we will start building the core functionality of the _Wealth-Wise_ Dashboard application. You will implement functions to handle financial transactions, calculate balances, and manage user budgets. This module forms the foundation of our application, so it's important to implement these functions carefully and thoroughly.

By the end of this tutorial, you will have created a working transactions module that can be used to track user financial data.

### Step 1: Check Out the tut-2 Branch

First, ensure you're working on the `tut-2` branch:
```bash
git checkout tut-2
```

### Step 2: Open the Transactions Module

1. In VSCode, navigate to the `transactions.py` file in the root directory of the project.
2. Open the file and review its structure. You should see several function definitions with `# TODO` comments and docstrings explaining what each function should do.

### Step 3: Understand the Functions

Before implementing, read the docstring for each function carefully. The docstrings explain:
- What the function should do
- What parameters it accepts
- What it should return
- Any important behavior or edge cases to handle

Take time to understand the requirements for each function before writing code.

### Step 4: Implement the Functions

For each function with a `# TODO` comment:
1. Read the docstring thoroughly
2. Implement the function logic based on the requirements
3. Test your implementation as you go (see Step 5)

### Step 5: Test Your Implementation

Once you have completed the functions in the `transactions.py` module, verify your implementation by running the unit tests:

1. Ensure you are in the root directory of the project
2. Make sure your virtual environment is activated
3. Run the tests using:
   ```bash
   pytest tests/test_transactions.py
   ```

This command will run all unit tests for the transactions module. You should see output indicating:
- How many tests were run
- How many tests passed or failed
- Detailed error messages if any tests failed

### Step 6: Debug and Fix Issues

If any tests fail:
1. Read the error message carefully to understand what went wrong
2. Review the corresponding test case in `tests/test_transactions.py`
3. Check your implementation logic
4. Make corrections and run the tests again

Repeat this process until all tests pass successfully.

### Step 7: Commit Your Work

Once all tests pass, commit your completed work to your repository:

1. Check the status of your changes:
   ```bash
   git status
   ```
2. Stage your changes:
   ```bash
   git add transactions.py
   ```
3. Commit with a meaningful message:
   ```bash
   git commit -m "Completed Tutorial 2: Implement transactions module"
   ```
4. Push your changes to the tut-2 branch:
   ```bash
   git push origin tut-2
   ```

---

Congratulations! You have successfully implemented the transactions module. You are now ready to proceed to Tutorial 3, where we will build additional features on top of this foundation.

Happy coding!




