"""Hard difficulty tasks - Subqueries and Window Functions."""

HARD_TASKS = [
    {
        "id": "hard_001",
        "question": "Find customers whose total spending exceeds the average",
        "difficulty": "hard",
        "ground_truth_sql": """
            SELECT c.id, c.name, c.email, SUM(o.total_amount) as total_spent
            FROM customers c
            JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name, c.email
            HAVING SUM(o.total_amount) > (
                SELECT AVG(total_spent) FROM (
                    SELECT customer_id, SUM(total_amount) as total_spent
                    FROM orders
                    GROUP BY customer_id
                )
            )
            ORDER BY total_spent DESC
        """,
        "expected_columns": ["id", "name", "email", "total_spent"],
        "grader": "sql_execution_grader",
    },
    {
        "id": "hard_002",
        "question": "Show the top 3 products by revenue in each category",
        "difficulty": "hard",
        "ground_truth_sql": """
            SELECT category, product_name, revenue, rank
            FROM (
                SELECT 
                    p.category,
                    p.name as product_name,
                    SUM(oi.quantity * oi.unit_price) as revenue,
                    ROW_NUMBER() OVER (PARTITION BY p.category ORDER BY SUM(oi.quantity * oi.unit_price) DESC) as rank
                FROM products p
                JOIN order_items oi ON p.id = oi.product_id
                GROUP BY p.id, p.category, p.name
            )
            WHERE rank <= 3
            ORDER BY category, revenue DESC
        """,
        "expected_columns": ["category", "product_name", "revenue", "rank"],
        "grader": "sql_execution_grader",
    },
    {
        "id": "hard_003",
        "question": "Find orders where total amount is above the median",
        "difficulty": "hard",
        "ground_truth_sql": """
            SELECT id, customer_id, order_date, total_amount
            FROM orders
            WHERE total_amount > (
                SELECT AVG(total_amount) FROM (
                    SELECT total_amount FROM orders ORDER BY total_amount
                    LIMIT 2 - (SELECT COUNT(*) FROM orders) / 2
                    OFFSET (SELECT COUNT(*) FROM orders) / 2 - 1
                )
            )
            ORDER BY total_amount DESC
        """,
        "expected_columns": ["id", "customer_id", "order_date", "total_amount"],
        "grader": "sql_execution_grader",
    },
]
