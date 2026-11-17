import os
import sys
import pandas as pd

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from config.mysql_db import get_mysql_connection


def seed_mysql_inventory():
  conn = get_mysql_connection()
  if not conn:
    return
  cursor = conn.cursor()
  data_dir = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", "data")
  )

  try:
    # Products
    products_df = pd.read_csv(os.path.join(data_dir, "products.csv"))
    for _, row in products_df.iterrows():
      cursor.execute(
          """
                INSERT INTO products (product_id, name, category, price, reorder_level)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE price=VALUES(price), reorder_level=VALUES(reorder_level)
            """,
          (
              row["product_id"],
              row["name"],
              row["category"],
              row["price"],
              row["reorder_level"],
          ),
      )

    # Warehouses
    warehouses_df = pd.read_csv(os.path.join(data_dir, "warehouses.csv"))
    for _, row in warehouses_df.iterrows():
      cursor.execute(
          """
                INSERT INTO warehouses (warehouse_id, warehouse_name, location)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE warehouse_name=VALUES(warehouse_name), location=VALUES(location)
            """,
          (row["warehouse_id"], row["warehouse_name"], row["location"]),
      )

    # Suppliers
    suppliers_df = pd.read_csv(os.path.join(data_dir, "suppliers.csv"))
    for _, row in suppliers_df.iterrows():
      cursor.execute(
          """
                INSERT INTO suppliers (supplier_id, supplier_name, contact_email, phone)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE supplier_name=VALUES(supplier_name), contact_email=VALUES(contact_email)
            """,
          (
              row["supplier_id"],
              row["supplier_name"],
              row["contact_email"],
              row["phone"],
          ),
      )

    # Stock Movements
    movements_df = pd.read_csv(os.path.join(data_dir, "stock_movements.csv"))
    for _, row in movements_df.iterrows():
      cursor.execute(
          """
                INSERT INTO stock_movements (movement_id, product_id, warehouse_id, supplier_id, movement_type, quantity, movement_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity=VALUES(quantity)
            """,
          (
              row["movement_id"],
              row["product_id"],
              row["warehouse_id"],
              row["supplier_id"],
              row["movement_type"],
              row["quantity"],
              row["movement_date"],
          ),
      )

    conn.commit()
    print("MySQL inventory seeding complete successfully!")
  except Exception as e:
    print(f"Error seeding MySQL: {e}")
    conn.rollback()
  finally:
    cursor.close()
    conn.close()


if __name__ == "__main__":
  seed_mysql_inventory()