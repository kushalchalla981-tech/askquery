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
    },
    {
        "id": "medium_004",
        "question": "What is the total revenue per customer?",
        "difficulty": "medium",
        "ground_truth_sql": """
            SELECT c.id, c.name, SUM(o.total_amount) as total_revenue
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name
            ORDER BY total_revenue DESC
        """,
        "expected_columns": ["id", "name", "total_revenue"],
    },
    {
        "id": "medium_005",
        "question": "Which products have been ordered more than 5 times?",
        "difficulty": "medium",
        "ground_truth_sql": """
            SELECT p.id, p.name, p.category, SUM(oi.quantity) as total_ordered
            FROM products p
            JOIN order_items oi ON p.id = oi.product_id
            GROUP BY p.id, p.name, p.category
            HAVING SUM(oi.quantity) > 5
            ORDER BY total_ordered DESC
        """,
        "expected_columns": ["id", "name", "category", "total_ordered"],
    },
    {
        "id": "medium_006",
        "question": "What is the average number of items per order?",
        "difficulty": "medium",
        "ground_truth_sql": """
            SELECT o.id as order_id, AVG(oi.quantity) as avg_items
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            GROUP BY o.id
            ORDER BY o.id
        """,
        "expected_columns": ["order_id", "avg_items"],
    },
]
