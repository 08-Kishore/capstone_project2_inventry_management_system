# =========================================================================
# Capstone Project: Inventory Management System
# Week 4: ETL Pipeline in Azure Databricks
# =========================================================================

import os
import pandas as pd # type: ignore


def run_databricks_etl_simulation():
  print("Starting Azure Databricks ETL Simulation...")

  # Define data directory paths
  current_dir = os.path.dirname(__file__)
  data_dir = os.path.abspath(os.path.join(current_dir, "..", "data"))

  products_path = os.path.join(data_dir, "products.csv")
  warehouses_path = os.path.join(data_dir, "warehouses.csv")
  movements_path = os.path.join(data_dir, "stock_movements.csv")

  if (
      not os.path.exists(products_path)
      or not os.path.exists(warehouses_path)
      or not os.path.exists(movements_path)
  ):
    print("Error: Missing one or more required input CSV datasets.")
    return

  # 1. Load cleaned stock and product data[cite: 5]
  products_df = pd.read_csv(products_path)
  warehouses_df = pd.read_csv(warehouses_path)
  movements_df = pd.read_csv(movements_path)

  # Compute current stock per product & warehouse from movements
  movements_df["signed_qty"] = movements_df.apply(
      lambda row: (
          row["quantity"] if row["movement_type"] == "IN" else -row["quantity"]
      ),
      axis=1,
  )
  stock_agg = (
      movements_df.groupby(["warehouse_id", "product_id"])["signed_qty"]
      .sum()
      .reset_index(name="current_stock")
  )

  # 2. Join product and warehouse info[cite: 5]
  master_df = stock_agg.merge(products_df, on="product_id", how="inner")
  master_df = master_df.merge(warehouses_df, on="warehouse_id", how="inner")

  # 3. Create a master inventory view with reorder flag[cite: 5]
  master_df["needs_reorder"] = (
      master_df["current_stock"] <= master_df["reorder_level"]
  )

  # Reorder and select key columns for dashboarding
  master_inventory_view = master_df[
      [
          "warehouse_id",
          "warehouse_name",
          "location",
          "product_id",
          "name",
          "category",
          "price",
          "reorder_level",
          "current_stock",
          "needs_reorder",
      ]
  ]

  print("\n--- Master Inventory View Sample ---")
  print(master_inventory_view.head(10))

  # 4. Save output in CSV / Delta format ready for dashboarding[cite: 5]
  output_dir = os.path.abspath(os.path.dirname(__file__))
  output_file = os.path.join(output_dir, "master_inventory_view.csv")
  master_inventory_view.to_csv(output_file, index=False)

  print(
      "\nETL Pipeline Completed Successfully! Master inventory view saved to:"
      f" {output_file}"
  )


if __name__ == "__main__":
  run_databricks_etl_simulation()