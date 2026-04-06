"""Easy difficulty tasks - Single-table SELECT with WHERE clause."""

EASY_TASKS = [
    {
        "id": "easy_001",
        "question": "Show all customers from California",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, name, email, city, state FROM customers WHERE state = 'CA'",
        "expected_columns": ["id", "name", "email", "city", "state"],
    },
    {
        "id": "easy_002",
        "question": "List all products in the Electronics category",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, name, category, price FROM products WHERE category = 'Electronics'",
        "expected_columns": ["id", "name", "category", "price"],
    },
    {
        "id": "easy_003",
        "question": "Find all orders with status 'shipped'",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, customer_id, order_date, total_amount FROM orders WHERE status = 'shipped'",
        "expected_columns": ["id", "customer_id", "order_date", "total_amount"],
    },
    {
        "id": "easy_004",
        "question": "Show customers from New York",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, name, email, city, state FROM customers WHERE state = 'NY'",
        "expected_columns": ["id", "name", "email", "city", "state"],
    },
    {
        "id": "easy_005",
        "question": "List all products with price under 50",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, name, category, price FROM products WHERE price < 50",
        "expected_columns": ["id", "name", "category", "price"],
    },
    {
        "id": "easy_006",
        "question": "Find all orders from June 2024",
        "difficulty": "easy",
        "ground_truth_sql": "SELECT id, customer_id, order_date, total_amount FROM orders WHERE order_date >= '2024-06-01' AND order_date < '2024-07-01'",
        "expected_columns": ["id", "customer_id", "order_date", "total_amount"],
    },
]
