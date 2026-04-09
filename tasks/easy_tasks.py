"""Easy difficulty tasks - Single-table SELECT with WHERE clause."""

EASY_TASKS = [
    {
        "id": "easy_001",
        "question": "Show all customers from California",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, name, email, city, state FROM customers WHERE state = 'CA'",
        "expected_columns": ["id", "name", "email", "city", "state"],
        "grader": "sql_execution_grader",
    },
    {
        "id": "easy_002",
        "question": "List all products in the Electronics category",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, name, category, price FROM products WHERE category = 'Electronics'",
        "expected_columns": ["id", "name", "category", "price"],
        "grader": "sql_execution_grader",
    },
    {
        "id": "easy_003",
        "question": "Find all orders with status 'shipped'",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, customer_id, order_date, total_amount FROM orders WHERE status = 'shipped'",
        "expected_columns": ["id", "customer_id", "order_date", "total_amount"],
        "grader": "sql_execution_grader",
    },
]
