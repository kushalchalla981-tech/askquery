"""Medium difficulty tasks - JOIN, GROUP BY, and Aggregations."""

MEDIUM_TASKS = [
    {
        "id": "medium_001",
        "question": "What is the total number of orders per customer?",
        "difficulty": "medium",
        "ground_truth_sql": """
            SELECT c.id, c.name, COUNT(o.id) as order_count 
            FROM customers c 
            LEFT JOIN orders o ON c.id = o.customer_id 
            GROUP BY c.id, c.name 
            ORDER BY order_count DESC
        """,
        "expected_columns": ["id", "name", "order_count"],
        "grader": "sql_execution_grader",
    },
    {
        "id": "medium_002",
        "question": "What is the average order value by product category?",
        "difficulty": "medium",
        "ground_truth_sql": """
            SELECT p.category, AVG(oi.unit_price * oi.quantity) as avg_order_value, COUNT(*) as total_items
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            GROUP BY p.category
            ORDER BY avg_order_value DESC
        """,
        "expected_columns": ["category", "avg_order_value", "total_items"],
        "grader": "sql_execution_grader",
    },
    {
        "id": "medium_003",
        "question": "How many products were sold in each state?",
        "difficulty": "medium",
        "ground_truth_sql": """
            SELECT c.state, COUNT(oi.id) as products_sold
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN customers c ON o.customer_id = c.id
            GROUP BY c.state
            ORDER BY products_sold DESC
        """,
        "expected_columns": ["state", "products_sold"],
        "grader": "sql_execution_grader",
    },
]
