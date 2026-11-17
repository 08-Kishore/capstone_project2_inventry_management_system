# =========================================================================
# Capstone Project: Inventory Management System
# Week 3: PySpark for Warehouse-Level Insights
# =========================================================================

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, when


def run_warehouse_analytics():
  # 1. Initialize Spark Session
  spark = (
      SparkSession.builder.appName("WarehouseInventoryAnalytics")
      .master("local[*]")
      .getOrCreate()
  )

  print("Spark Session initialized successfully.")

  # Define path to dataset
  current_dir = os.path.dirname(__file__)
  csv_path = os.path.abspath(
      os.path.join(current_dir, "..", "data", "stock_movements.csv")
  )

  if not os.path.exists(csv_path):
    print(f"Error: Could not locate {csv_path}")
    spark.stop()
    return

  # 2. Load large stock movement data using PySpark[cite: 5]
  df = (
      spark.read.option("header", "true")
      .option("inferSchema", "true")
      .csv(csv_path)
  )

  print(f"Loaded {df.count()} stock movement records.")

  # 3. Transform movement types to signed quantities (+ for IN, - for OUT/ADJUSTMENT)
  df_transformed = df.withColumn(
      "signed_qty",
      when(col("movement_type") == "IN", col("quantity")).otherwise(
          -col("quantity")
      ),
  )

  # 4. Aggregate total stock per warehouse and product[cite: 5]
  warehouse_product_summary = df_transformed.groupBy(
      "warehouse_id", "product_id"
  ).agg(sum("signed_qty").alias("net_stock"))

  # 5. Identify overstocked or understocked items using filter logic[cite: 5]
  # Defining rules: understocked if net_stock < 5, overstocked if net_stock > 50
  status_df = warehouse_product_summary.withColumn(
      "stock_status",
      when(col("net_stock") < 5, "UNDERSTOCKED")
      .when(col("net_stock") > 50, "OVERSTOCKED")
      .otherwise("OPTIMAL"),
  )

  print("\n--- Warehouse-Level Stock Status Sample ---")
  status_df.show(10)

  # 6. Output file with warehouse-level stock status[cite: 5]
  output_dir = os.path.abspath(os.path.join(current_dir, "output"))
  os.makedirs(output_dir, exist_ok=True)
  output_csv_path = os.path.join(output_dir, "warehouse_stock_status.csv")

  # Write back to CSV (coalesce to single file for easy retrieval)
  status_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(
      output_dir
  )
  print(
      f"Warehouse-level stock status successfully generated at: {output_dir}"
  )

  spark.stop()


if __name__ == "__main__":
  run_warehouse_analytics()