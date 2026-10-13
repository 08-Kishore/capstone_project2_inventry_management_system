import os
import sys

# pyright: reportMissingModuleSource=false
import pandas as pd  # type: ignore[import-not-found]

# Add project root to path so we can import from the config folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.mysql_db import get_mysql_connection

def seed_mysql_inventory():
    # 1. Connect to MySQL database using config module
    conn = get_mysql_connection()
    if not conn:
        print("Error: Could not establish a MySQL connection.")
        return

    cursor = conn.cursor()
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

    try:
        # 2. Load and insert Products (50 sample records)
        products_path = os.path.join(data_dir, "products.csv")
        if os.path.exists(products_path):
            products_df = pd.read_csv(products_path)
            for _, row in products_df.iterrows():
                cursor.execute("""
                    INSERT INTO products (product_id, name, category, price, reorder_level)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE price=VALUES(price), reorder_level=VALUES(reorder_level)
                """, (row["product_id"], row["name"], row["category"], row["price"], row["reorder_level"]))
            print(f"Successfully inserted {len(products_df)} products into MySQL!")

        # 3. Load and insert Warehouses
        warehouses_path = os.path.join(data_dir, "warehouses.csv")
        if os.path.exists(warehouses_path):
            warehouses_df = pd.read_csv(warehouses_path)
            for _, row in warehouses_df.iterrows():
                cursor.execute("""
                    INSERT INTO warehouses (warehouse_id, warehouse_name, location)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE warehouse_name=VALUES(warehouse_name), location=VALUES(location)
                """, (row["warehouse_id"], row["warehouse_name"], row["location"]))
            print(f"Successfully inserted {len(warehouses_df)} warehouses into MySQL!")

        # 4. Load and insert Suppliers
        suppliers_path = os.path.join(data_dir, "suppliers.csv")
        if os.path.exists(suppliers_path):
            suppliers_df = pd.read_csv(suppliers_path)
            for _, row in suppliers_df.iterrows():
                cursor.execute("""
                    INSERT INTO suppliers (supplier_id, supplier_name, contact_email, phone)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE supplier_name=VALUES(supplier_name), contact_email=VALUES(contact_email)
                """, (row["supplier_id"], row["supplier_name"], row["contact_email"], row["phone"]))
            print(f"Successfully inserted {len(suppliers_df)} suppliers into MySQL!")

        # 5. Load and insert Stock Movements
        movements_path = os.path.join(data_dir, "stock_movements.csv")
        if os.path.exists(movements_path):
            movements_df = pd.read_csv(movements_path)
            for _, row in movements_df.iterrows():
                cursor.execute("""
                    INSERT INTO stock_movements (movement_id, product_id, warehouse_id, supplier_id, movement_type, quantity, movement_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE quantity=VALUES(quantity)
                """, (row["movement_id"], row["product_id"], row["warehouse_id"], row["supplier_id"], row["movement_type"], row["quantity"], row["movement_date"]))
            print(f"Successfully inserted {len(movements_df)} stock movements into MySQL!")

        conn.commit()
        print("MySQL inventory seeding complete!")

    except Exception as e:
        print(f"Error seeding MySQL data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_mysql_inventory()