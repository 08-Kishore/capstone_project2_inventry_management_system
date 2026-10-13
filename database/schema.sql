
CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

-- Drop tables in reverse order of dependencies to ensure clean re-runs
DROP TABLE IF EXISTS stock_movements;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS products;


-- Products Table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    reorder_level INT NOT NULL
);

-- Warehouses Table
CREATE TABLE warehouses (
    warehouse_id INT PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL
);

-- Suppliers Table
CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100),
    phone VARCHAR(20)
);

-- Stock Movements Table
CREATE TABLE stock_movements (
    movement_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    warehouse_id INT,
    supplier_id INT,
    movement_type ENUM('IN', 'OUT', 'ADJUSTMENT') NOT NULL,
    quantity INT NOT NULL,
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);


-- Indexes for quick search by product category, product ID, or warehouse
CREATE INDEX idx_product_category ON products(category);
CREATE INDEX idx_movement_product ON stock_movements(product_id);
CREATE INDEX idx_movement_warehouse ON stock_movements(warehouse_id);


DELIMITER //

-- Stored procedure to identify products below or at their reorder level
CREATE PROCEDURE GetProductsBelowReorderLevel()
BEGIN
    SELECT 
        p.product_id,
        p.name AS product_name,
        p.category,
        p.reorder_level,
        COALESCE(SUM(CASE WHEN sm.movement_type = 'IN' THEN sm.quantity ELSE -sm.quantity END), 0) AS current_stock
    FROM products p
    LEFT JOIN stock_movements sm ON p.product_id = sm.product_id
    GROUP BY p.product_id, p.name, p.category, p.reorder_level
    HAVING current_stock <= p.reorder_level;
END //

DELIMITER ;