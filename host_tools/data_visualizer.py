#!/usr/bin/env python3
  """
  data_visualizer.py — Plot wildlife detection logs from SD card CSV.

  Usage:
      python host_tools/data_visualizer.py --csv DETECTIONS/log_00012345.csv
  """
  import argparse
  from pathlib import Path
  import pandas as pd
  import matplotlib.pyplot as plt

  def visualize(csv_path: str):
      df = pd.read_csv(csv_path)
      print(f"Loaded {len(df)} detections from {csv_path}")
      print(df.head(10))

      species_counts = df["species"].value_counts().head(15)
      fig, axes = plt.subplots(1, 2, figsize=(14, 6))

      species_counts.plot(kind="barh", ax=axes[0], color="steelblue")
      axes[0].set_title("Top 15 Detected Species")
      axes[0].set_xlabel("Detection Count")
      axes[0].invert_yaxis()

      df["confidence"].plot(kind="hist", bins=20, ax=axes[1], color="darkorange")
      axes[1].set_title("Confidence Score Distribution")
      axes[1].set_xlabel("Confidence")

      plt.tight_layout()
      out = Path(csv_path).stem + "_report.png"
      plt.savefig(out, dpi=150)
      print(f"Report saved: {out}")
      plt.show()

  def main():
      p = argparse.ArgumentParser()
      p.add_argument("--csv", required=True)
      args = p.parse_args()
      if not Path(args.csv).exists(): print(f"File not found: {args.csv}"); return
      visualize(args.csv)

  if __name__ == "__main__":
      main()
  