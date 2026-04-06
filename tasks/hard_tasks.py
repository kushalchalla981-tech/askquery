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
    },
    {
        "id": "hard_004",
        "question": "Show customers with their order count and rank by spending",
        "difficulty": "hard",
        "ground_truth_sql": """
            SELECT 
                c.id,
                c.name,
                c.state,
                COUNT(o.id) as order_count,
                SUM(o.total_amount) as total_spent,
                RANK() OVER (ORDER BY SUM(o.total_amount) DESC) as spending_rank
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id, c.name, c.state
            ORDER BY spending_rank
        """,
        "expected_columns": [
            "id",
            "name",
            "state",
            "order_count",
            "total_spent",
            "spending_rank",
        ],
    },
    {
        "id": "hard_005",
        "question": "Find products that are performing below their category average",
        "difficulty": "hard",
        "ground_truth_sql": """
            SELECT p.id, p.name, p.category, p.price, category_avg
            FROM products p
            JOIN (
                SELECT category, AVG(price) as category_avg
                FROM products
                GROUP BY category
            ) ca ON p.category = ca.category
            WHERE p.price < ca.category_avg
            ORDER BY p.category, p.price
        """,
        "expected_columns": ["id", "name", "category", "price", "category_avg"],
    },
    {
        "id": "hard_006",
        "question": "Show month-over-month revenue growth for each category",
        "difficulty": "hard",
        "ground_truth_sql": """
            SELECT 
                strftime('%Y-%m', o.order_date) as month,
                p.category,
                SUM(oi.quantity * oi.unit_price) as revenue,
                LAG(SUM(oi.quantity * oi.unit_price)) OVER (PARTITION BY p.category ORDER BY strftime('%Y-%m', o.order_date)) as prev_month_revenue,
                ROUND((SUM(oi.quantity * oi.unit_price) - LAG(SUM(oi.quantity * oi.unit_price)) OVER (PARTITION BY p.category ORDER BY strftime('%Y-%m', o.order_date))) * 100.0 / NULLIF(LAG(SUM(oi.quantity * oi.unit_price)) OVER (PARTITION BY p.category ORDER BY strftime('%Y-%m', o.order_date)), 0), 2) as growth_pct
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN products p ON oi.product_id = p.id
            GROUP BY strftime('%Y-%m', o.order_date), p.category
            ORDER BY month, p.category
        """,
        "expected_columns": [
            "month",
            "category",
            "revenue",
            "prev_month_revenue",
            "growth_pct",
        ],
    },
]
