import os
import numpy as np
import pandas as pd


def process_stock_movements():
  data_dir = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", "data")
  )
  csv_path = os.path.join(data_dir, "stock_movements.csv")

  df = pd.read_csv(csv_path)
  df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
  df["quantity"] = df["quantity"].astype(int)

  # Vectorized calculation using NumPy
  df["signed_qty"] = np.where(
      df["movement_type"] == "IN", df["quantity"], -df["quantity"]
  )
  stock_summary = df.groupby("product_id")["signed_qty"].sum()
  summary_df = stock_summary.reset_index(name="current_stock")

  # Flag items below threshold using Pandas
  low_stock_threshold = 10
  summary_df["is_low_stock"] = summary_df["current_stock"] < low_stock_threshold
  low_stock_items = summary_df[summary_df["is_low_stock"]]

  print(f"\n--- Low-Stock Alert Report (Threshold < {low_stock_threshold}) ---")
  print(low_stock_items)

  report_path = os.path.join(os.path.dirname(__file__), "low_stock_report.csv")
  low_stock_items.to_csv(report_path, index=False)
  print(f"Low-stock report saved to: {report_path}")


if __name__ == "__main__":
  process_stock_movements()