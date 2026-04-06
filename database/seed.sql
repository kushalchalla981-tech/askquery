-- Seed data for Text-to-SQL E-commerce Database

-- Insert Customers (20+ customers across 8+ US states)
INSERT INTO customers (id, name, email, city, state, created_at) VALUES
(1, 'John Smith', 'john.smith@email.com', 'Los Angeles', 'CA', '2024-01-15'),
(2, 'Sarah Johnson', 'sarah.j@email.com', 'New York', 'NY', '2024-02-20'),
(3, 'Michael Brown', 'm.brown@email.com', 'Chicago', 'IL', '2024-03-10'),
(4, 'Emily Davis', 'emily.d@email.com', 'Houston', 'TX', '2024-01-25'),
(5, 'David Wilson', 'd.wilson@email.com', 'Phoenix', 'AZ', '2024-04-05'),
(6, 'Jessica Taylor', 'j.taylor@email.com', 'Philadelphia', 'PA', '2024-02-28'),
(7, 'Robert Anderson', 'r.anderson@email.com', 'San Antonio', 'TX', '2024-03-15'),
(8, 'Amanda Martinez', 'a.martinez@email.com', 'San Diego', 'CA', '2024-05-01'),
(9, 'Christopher Lee', 'c.lee@email.com', 'Dallas', 'TX', '2024-01-30'),
(10, 'Jennifer White', 'j.white@email.com', 'San Jose', 'CA', '2024-04-20'),
(11, 'Matthew Harris', 'm.harris@email.com', 'Austin', 'TX', '2024-02-10'),
(12, 'Ashley Clark', 'a.clark@email.com', 'Jacksonville', 'FL', '2024-03-25'),
(13, 'Daniel Lewis', 'd.lewis@email.com', 'Fort Worth', 'TX', '2024-05-10'),
(14, 'Stephanie Walker', 's.walker@email.com', 'Columbus', 'OH', '2024-01-20'),
(15, 'Andrew Hall', 'a.hall@email.com', 'Charlotte', 'NC', '2024-04-15'),
(16, 'Nicole Young', 'n.young@email.com', 'Seattle', 'WA', '2024-02-05'),
(17, 'Joshua King', 'j.king@email.com', 'Denver', 'CO', '2024-03-30'),
(18, 'Elizabeth Wright', 'e.wright@email.com', 'Boston', 'MA', '2024-05-15'),
(19, 'Ryan Scott', 'r.scott@email.com', 'Portland', 'OR', '2024-01-10'),
(20, 'Megan Green', 'm.green@email.com', 'Miami', 'FL', '2024-04-25'),
(21, 'Kevin Baker', 'k.baker@email.com', 'Atlanta', 'GA', '2024-02-15'),
(22, 'Laura Adams', 'l.adams@email.com', 'Sacramento', 'CA', '2024-03-20');

-- Insert Products (15+ products across 4+ categories)
INSERT INTO products (id, name, category, price, stock_quantity) VALUES
(1, 'Laptop Pro 15', 'Electronics', 1299.99, 50),
(2, 'Wireless Mouse', 'Electronics', 29.99, 200),
(3, 'USB-C Cable', 'Electronics', 15.99, 500),
(4, 'Mechanical Keyboard', 'Electronics', 149.99, 75),
(5, 'Monitor 27 inch', 'Electronics', 399.99, 30),
(6, 'Running Shoes', 'Sports', 89.99, 100),
(7, 'Yoga Mat', 'Sports', 24.99, 150),
(8, 'Tennis Racket', 'Sports', 129.99, 40),
(9, 'Fitness Tracker', 'Sports', 79.99, 80),
(10, 'Basketball', 'Sports', 29.99, 60),
(11, 'Python Programming', 'Books', 49.99, 200),
(12, 'Data Science Handbook', 'Books', 39.99, 120),
(13, 'Machine Learning Guide', 'Books', 59.99, 90),
(14, 'SQL Mastery', 'Books', 34.99, 150),
(15, 'Web Development', 'Books', 44.99, 110),
(16, 'Office Chair', 'Furniture', 249.99, 25),
(17, 'Standing Desk', 'Furniture', 599.99, 15),
(18, 'Desk Lamp', 'Furniture', 39.99, 80);

-- Insert Orders (30+ orders with varying dates and statuses)
INSERT INTO orders (id, customer_id, order_date, total_amount, status) VALUES
(1, 1, '2024-06-01', 1329.98, 'delivered'),
(2, 2, '2024-06-02', 89.99, 'shipped'),
(3, 3, '2024-06-03', 1449.98, 'delivered'),
(4, 4, '2024-06-04', 74.98, 'pending'),
(5, 5, '2024-06-05', 399.99, 'delivered'),
(6, 6, '2024-06-06', 179.98, 'shipped'),
(7, 7, '2024-06-07', 1344.98, 'delivered'),
(8, 8, '2024-06-08', 54.98, 'pending'),
(9, 9, '2024-06-09', 159.98, 'delivered'),
(10, 10, '2024-06-10', 429.98, 'shipped'),
(11, 1, '2024-06-11', 44.99, 'delivered'),
(12, 11, '2024-06-12', 99.98, 'pending'),
(13, 12, '2024-06-13', 279.98, 'delivered'),
(14, 13, '2024-06-14', 629.98, 'shipped'),
(15, 14, '2024-06-15', 114.98, 'delivered'),
(16, 15, '2024-06-16', 149.99, 'delivered'),
(17, 16, '2024-06-17', 79.99, 'shipped'),
(18, 17, '2024-06-18', 639.98, 'delivered'),
(19, 18, '2024-06-19', 94.98, 'pending'),
(20, 19, '2024-06-20', 109.98, 'delivered'),
(21, 20, '2024-06-21', 69.98, 'delivered'),
(22, 21, '2024-06-22', 489.98, 'shipped'),
(23, 22, '2024-06-23', 84.98, 'pending'),
(24, 2, '2024-06-24', 179.98, 'delivered'),
(25, 3, '2024-06-25', 129.99, 'shipped'),
(26, 4, '2024-06-26', 219.98, 'delivered'),
(27, 5, '2024-06-27', 59.98, 'delivered'),
(28, 6, '2024-06-28', 399.99, 'pending'),
(29, 7, '2024-06-29', 164.98, 'delivered'),
(30, 8, '2024-06-30', 124.98, 'shipped'),
(31, 9, '2024-07-01', 229.98, 'delivered'),
(32, 10, '2024-07-02', 74.98, 'delivered'),
(33, 11, '2024-07-03', 154.99, 'pending'),
(34, 12, '2024-07-04', 89.99, 'delivered'),
(35, 13, '2024-07-05', 199.98, 'shipped');

-- Insert Order Items (50+ items linking orders to products)
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES
-- Order 1
(1, 1, 1, 1, 1299.99),
(2, 1, 2, 1, 29.99),
-- Order 2
(3, 2, 6, 1, 89.99),
-- Order 3
(4, 3, 1, 1, 1299.99),
(5, 3, 3, 3, 15.99),
-- Order 4
(6, 4, 7, 2, 24.99),
(7, 4, 4, 1, 149.99),
-- Order 5
(8, 5, 5, 1, 399.99),
-- Order 6
(9, 6, 6, 1, 89.99),
(10, 6, 8, 1, 129.99),
-- Order 7
(11, 7, 1, 1, 1299.99),
(12, 7, 2, 3, 29.99),
-- Order 8
(13, 8, 11, 1, 49.99),
(14, 8, 12, 1, 39.99),
-- Order 9
(15, 9, 9, 1, 79.99),
(16, 9, 10, 2, 29.99),
-- Order 10
(17, 10, 5, 1, 399.99),
(18, 10, 4, 1, 149.99),
-- Order 11
(19, 11, 14, 1, 34.99),
(20, 11, 15, 1, 44.99),
-- Order 12
(21, 12, 9, 1, 79.99),
(22, 12, 7, 2, 24.99),
-- Order 13
(23, 13, 16, 1, 249.99),
(24, 13, 18, 1, 39.99),
-- Order 14
(25, 14, 17, 1, 599.99),
(26, 14, 18, 1, 39.99),
-- Order 15
(27, 15, 6, 1, 89.99),
(28, 15, 7, 1, 24.99),
-- Order 16
(29, 16, 4, 1, 149.99),
-- Order 17
(30, 17, 9, 1, 79.99),
-- Order 18
(31, 18, 17, 1, 599.99),
(32, 18, 3, 2, 15.99),
-- Order 19
(33, 19, 11, 1, 49.99),
(34, 19, 13, 1, 59.99),
-- Order 20
(35, 20, 7, 2, 24.99),
(36, 20, 10, 2, 29.99),
-- Order 21
(37, 21, 8, 1, 129.99),
(38, 21, 9, 1, 79.99),
-- Order 22
(39, 22, 16, 1, 249.99),
(40, 22, 18, 2, 39.99),
-- Order 23
(41, 23, 12, 1, 39.99),
(42, 23, 14, 1, 34.99),
-- Order 24
(43, 24, 6, 1, 89.99),
(44, 24, 10, 2, 29.99),
-- Order 25
(45, 25, 8, 1, 129.99),
-- Order 26
(46, 26, 16, 1, 249.99),
(47, 26, 18, 2, 39.99),
-- Order 27
(48, 27, 14, 1, 34.99),
(49, 27, 15, 1, 44.99),
-- Order 28
(50, 28, 5, 1, 399.99),
-- Order 29
(51, 29, 6, 1, 89.99),
(52, 29, 7, 1, 24.99),
(53, 29, 10, 1, 29.99),
-- Order 30
(54, 30, 11, 1, 49.99),
(55, 30, 12, 1, 39.99),
(56, 30, 13, 1, 59.99),
-- Order 31
(57, 31, 1, 1, 1299.99),
(58, 31, 4, 1, 149.99),
-- Order 32
(59, 32, 7, 2, 24.99),
(60, 32, 10, 1, 29.99),
-- Order 33
(61, 33, 4, 1, 149.99),
-- Order 34
(62, 34, 6, 1, 89.99),
-- Order 35
(63, 35, 16, 1, 249.99),
(64, 35, 18, 2, 39.99);