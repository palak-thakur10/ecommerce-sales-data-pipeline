-- ============================================================
-- E-COMMERCE SALES DATA ANALYSIS
-- ============================================================


-- 1. Total Revenue
SELECT
    ROUND(SUM(Revenue), 2) AS total_revenue
FROM sales;


-- 2. Total Units Sold
SELECT
    SUM(Quantity) AS total_units
FROM sales;


-- 3. Total Orders
SELECT
    COUNT(DISTINCT InvoiceNo) AS total_orders
FROM sales;


-- 4. Unique Customers
SELECT
    COUNT(DISTINCT CustomerID) AS unique_customers
FROM sales
WHERE CustomerID IS NOT NULL;


-- 5. Unique Products
SELECT
    COUNT(DISTINCT StockCode) AS unique_products
FROM sales;


-- 6. Revenue by Country
SELECT
    Country,
    ROUND(SUM(Revenue), 2) AS revenue,
    SUM(Quantity) AS units_sold,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
GROUP BY Country
ORDER BY revenue DESC;


-- 7. Top 10 Products by Revenue
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Revenue), 2) AS revenue,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
GROUP BY
    StockCode,
    Description
ORDER BY revenue DESC
LIMIT 10;


-- 8. Top 10 Customers by Revenue
SELECT
    CustomerID,
    ROUND(SUM(Revenue), 2) AS revenue,
    SUM(Quantity) AS units_purchased,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY revenue DESC
LIMIT 10;


-- 9. Monthly Sales Performance
SELECT
    strftime('%Y-%m', InvoiceDate) AS month,
    ROUND(SUM(Revenue), 2) AS revenue,
    SUM(Quantity) AS units_sold,
    COUNT(DISTINCT InvoiceNo) AS orders,
    COUNT(DISTINCT CustomerID) AS customers
FROM sales
GROUP BY strftime('%Y-%m', InvoiceDate)
ORDER BY month;


-- 10. Average Order Value
SELECT
    ROUND(
        SUM(Revenue) /
        COUNT(DISTINCT InvoiceNo),
        2
    ) AS average_order_value
FROM sales;


-- 11. Daily Revenue
SELECT
    DATE(InvoiceDate) AS sales_date,
    ROUND(SUM(Revenue), 2) AS revenue,
    SUM(Quantity) AS units_sold,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
GROUP BY DATE(InvoiceDate)
ORDER BY sales_date;


-- 12. Highest Revenue Orders
SELECT
    InvoiceNo,
    CustomerID,
    Country,
    ROUND(SUM(Revenue), 2) AS order_value
FROM sales
GROUP BY
    InvoiceNo,
    CustomerID,
    Country
ORDER BY order_value DESC
LIMIT 10;