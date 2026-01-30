# ECO5040S - Financial Software Engineering
Welcome to the repository for ECO5040S - Financial Software Engineering. This course focuses on the principles and practices of software engineering in the context of financial applications.

This course will be taught using Python as the primary programming language, along with relevant libraries and frameworks commonly used in the financial industry.

During this course, students will learn about software development methodologies, version control, testing, and deployment strategies tailored for financial systems. We will explore various topics by completing eight practical assignments that cover different aspects of financial software engineering. The goal is for each student to eventually create a personal finance app, _Wealth-Wise_. The overview of each tutorial is as follows:

## Tutorial Overview

### Tutorial 1: Setting Up Your Development Environment
- Introduction to Visual Studio Code (VSCode)
- Installing Python and necessary libraries (e.g., NumPy, Pandas, Matplotlib)
- Setting up Git and GitHub for version control
- Creating your first Python script
- Forking, merging, and pull requests on GitHub
- Basic command line operations
- Setting up a virtual environment

**Key Concepts: IDEs, version control, virtual environments, and package management.**

### Tutorial 2: Python Fundamentals & Financial Logic
- Kickstart the _Wealth-Wise_ Dashboard by building the core arithmetic engine.
- Focus on creating a robust script that handles basic transaction lists, performs currency formatting for Rand (R) values, and implements fundamental control flow for budget tracking.

**Key Concepts: Data types (floats vs. decimals), list comprehensions, and input/output.**

### Tutorial 3: Modular Programming & Style Guides
- Refactor your initial scripts into reusable functions and classes.
- Introduce the PEP 8 style guide and the concept of "Clean Code."
- Define a `Transaction` class to standardize how financial data is handled across the application.

**Key Concepts: Type hinting, docstrings, and class structures.**

### Tutorial 4: Defensive Programming & Unit Testing
- Financial software cannot afford to fail.
- Learn to use try-except blocks to handle "dirty" data and write your first unit tests using pytest.
- Implement environment variables for configuration management.

**Key Concepts: Exception handling, assertions, and test-driven development (TDD).**

### Tutorial 5: Relational Databases with SQLite
- Transition from temporary lists to permanent storage.
- Design a schema for your personal finance data, including tables for Categories and Transactions, and learn to interact with them using SQL within Python.

**Key Concepts: CRUD operations (Create, Read, Update, Delete), Primary Keys, and Foreign Keys.**   

### Tutorial 6: Data Analysis with Pandas & Matplotlib
- Unlock insights from your spending history.
- Use `Pandas` to aggregate your SQLite data to find monthly trends.
- Generate visual reports, such as spending pie charts, saved as static images using `Matplotlib`.

**Key Concepts: DataFrames, GroupBy operations, and data visualization.**   

### Tutorial 7: Backend API Development with Flask
- Turn your logic into a service.
- Build a RESTful API using `Flask` that serves your financial data as JSON.
- Allow other applications (or your future frontend) to "consume" your data programmatically.

**Key Concepts: Routes, HTTP Methods (GET/POST), and JSON serialization.**

### Tutorial 8: Full-Stack Integration & Jinja2
- Build the user interface.
- Use `Flask` to serve HTML templates and render the charts generated in Tutorial 6.
- Merge your separate components into a cohesive web application.

**Key Concepts: Template inheritance, serving static files (images/CSS), and request handling.**

### Tutorial 9: CI/CD & API Design Principles
- Finalize your project by implementing Continuous Integration.
- Set up a GitHub Action to automatically run your test suite every time you push code.
- Refine your API design to ensure it follows industry standards.

**Key Concepts: GitHub Actions, YAML configuration, and versioning.**

### Tutorial 10: Asynchronous Tasks with Celery
- Enhance your application with background processing.
- Use Celery to offload time-consuming tasks, such as generating reports or sending email notifications, to improve the responsiveness of your application.

**Key Concepts: Task queues, brokers (e.g., Redis), and asynchronous programming.**

### Tutorial 11: Deployment & Cloud Hosting
- Deploy your application to the cloud.
- Learn to use platforms like Render or Heroku to host your Flask application, making it accessible from anywhere.

**Key Concepts: Deployment pipelines, environment variables in production, and cloud services.**

### Tutorial 12: Introduction to Vibe Coding with Claude
- Explore the emerging field of AI-assisted coding.
- Learn how to leverage AI tools like Claude to enhance your coding efficiency and problem-solving skills.

**Key Concepts: AI-assisted coding, prompt engineering, and ethical considerations.**


## Branching Strategy
To maintain a clean and organized codebase, we will use the following branching strategy:
- `main`: The stable branch containing the latest production-ready code.
- `tutorial-1`, `tutorial-2`, ..., `tutorial-9`: Feature branches for each tutorial assignment. Students will create and work on these branches before merging them into `main` after completing each tutorial.

Each student is expected to fork the repository, which will allow them to work independently on their assignments while still being able to pull updates from the main repository if needed.

## Important Notes
- Software is sensitive to _spaces_ and _tabs_. Wherever possible, make sure your _path_ and _file names_ do not contain spaces.
- Always commit your changes with meaningful messages to keep track of your progress, "e.g., 'Implemented Transaction class in Tutorial 3'."
- Regularly push your changes to GitHub to avoid losing work.
- Feel free to reach out to [Marc](mailto:LVNMAR013@myuct.ac.za) if you encounter any issues or have questions about the assignments.

## Links and Resources
[Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions) - Recommended Python distribution for managing packages and environments.
[VSCode](https://code.visualstudio.com/download) - Integrated Development Environment (IDE) for coding.
[GitHub](https://github.com) - Platform for version control and collaboration.


## Conclusion
By the end of this course, students will have a solid foundation in financial software engineering and a functional personal finance application to showcase their skills. Happy coding!


