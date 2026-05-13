#!/usr/bin/env python3
  """
  validate_tensors.py
  Verify a TFLite model's input/output tensors match the expected shapes
  for SpeciesNet deployment on AMB82-Mini.
  """
  import argparse
  import sys
  import numpy as np

  try:
      import tflite_runtime.interpreter as tflite
  except ImportError:
      import tensorflow as tf
      tflite = tf.lite

  EXPECTED_INPUT_SHAPE  = (1, 320, 320, 3)
  EXPECTED_INPUT_DTYPE  = np.int8
  EXPECTED_OUTPUT_DTYPE = np.int8
  MIN_OUTPUT_CLASSES    = 100   # SpeciesNet has 1000+; stub has 1000

  def validate(model_path: str) -> bool:
      print(f"Validating: {model_path}")
      interp = tflite.Interpreter(model_path=model_path)
      interp.allocate_tensors()

      inp = interp.get_input_details()[0]
      out = interp.get_output_details()[0]

      ok = True

      # Check input shape
      shape = tuple(inp["shape"])
      if shape != EXPECTED_INPUT_SHAPE:
          print(f"  [FAIL] Input shape {shape} != expected {EXPECTED_INPUT_SHAPE}")
          ok = False
      else:
          print(f"  [OK]   Input shape:  {shape}")

      # Check input dtype (INT8)
      if inp["dtype"] != EXPECTED_INPUT_DTYPE:
          print(f"  [FAIL] Input dtype {inp['dtype']} != int8")
          ok = False
      else:
          print(f"  [OK]   Input dtype:  int8")

      # Check output dtype (INT8)
      if out["dtype"] != EXPECTED_OUTPUT_DTYPE:
          print(f"  [FAIL] Output dtype {out['dtype']} != int8")
          ok = False
      else:
          print(f"  [OK]   Output dtype: int8")

      # Check output class count
      num_classes = out["shape"][-1]
      if num_classes < MIN_OUTPUT_CLASSES:
          print(f"  [FAIL] Output classes {num_classes} < minimum {MIN_OUTPUT_CLASSES}")
          ok = False
      else:
          print(f"  [OK]   Output classes: {num_classes}")

      # Run a dummy inference to confirm no runtime errors
      dummy = np.zeros(EXPECTED_INPUT_SHAPE, dtype=np.int8)
      interp.set_tensor(inp["index"], dummy)
      interp.invoke()
      output = interp.get_tensor(out["index"])
      print(f"  [OK]   Dummy inference passed — output shape: {output.shape}")

      return ok

  def main():
      p = argparse.ArgumentParser()
      p.add_argument("--model", required=True)
      args = p.parse_args()
      success = validate(args.model)
      print("\nValidation:", "PASSED" if success else "FAILED")
      sys.exit(0 if success else 1)

  if __name__ == "__main__":
      main()
  