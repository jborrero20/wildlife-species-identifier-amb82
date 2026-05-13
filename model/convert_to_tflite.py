#!/usr/bin/env python3
  """
  convert_to_tflite.py — Convert SpeciesNet SavedModel to INT8 TFLite
  for deployment on the AMB82-Mini NPU.

  Usage:
      python model/convert_to_tflite.py --output model/speciesnet_int8.tflite
  """
  import argparse
  import numpy as np
  import tensorflow as tf
  from pathlib import Path

  IMAGE_SIZE = (320, 320)
  NUM_CALIBRATION = 100


  def representative_dataset():
      for _ in range(NUM_CALIBRATION):
          yield [np.random.uniform(0, 1, (1, *IMAGE_SIZE, 3)).astype(np.float32)]


  def convert(output_path: Path, saved_model_dir: Path):
      converter = tf.lite.TFLiteConverter.from_saved_model(str(saved_model_dir))
      converter.optimizations = [tf.lite.Optimize.DEFAULT]
      converter.representative_dataset = representative_dataset
      converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
      converter.inference_input_type  = tf.int8
      converter.inference_output_type = tf.int8

      print("Converting SpeciesNet → INT8 TFLite...")
      model = converter.convert()
      output_path.parent.mkdir(parents=True, exist_ok=True)
      output_path.write_bytes(model)
      print(f"Saved: {output_path}  ({len(model)/1024/1024:.2f} MB)")


  def main():
      p = argparse.ArgumentParser()
      p.add_argument("--saved_model", default="model/speciesnet_saved_model")
      p.add_argument("--output",      default="model/speciesnet_int8.tflite")
      args = p.parse_args()
      saved = Path(args.saved_model)
      if not saved.exists():
          print(f"[ERROR] SavedModel not found: {saved}")
          return 1
      convert(Path(args.output), saved)
      return 0

  if __name__ == "__main__":
      raise SystemExit(main())
  