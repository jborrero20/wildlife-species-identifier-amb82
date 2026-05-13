#!/usr/bin/env python3
  """
  validate_model.py — Run INT8 TFLite SpeciesNet on a test image.

  Usage:
      python model/validate_model.py --model model/speciesnet_int8.tflite \
                                     --image test_images/deer.jpg
  """
  import argparse
  import numpy as np
  from pathlib import Path

  try:
      import tflite_runtime.interpreter as tflite
  except ImportError:
      import tensorflow as tf
      tflite = tf.lite

  from PIL import Image


  def preprocess(path, size):
      img = Image.open(path).convert("RGB").resize(size)
      return np.expand_dims(np.array(img, dtype=np.float32) / 255.0, 0)


  def run(model_path, image_path, top_k=5):
      interp = tflite.Interpreter(model_path=model_path)
      interp.allocate_tensors()
      inp = interp.get_input_details()[0]
      out = interp.get_output_details()[0]
      h, w = inp["shape"][1], inp["shape"][2]
      data = preprocess(image_path, (w, h))
      if inp["dtype"] == np.int8:
          s, z = inp["quantization"]
          data = (data / s + z).astype(np.int8)
      interp.set_tensor(inp["index"], data)
      interp.invoke()
      output = interp.get_tensor(out["index"])[0]
      if out["dtype"] == np.int8:
          s, z = out["quantization"]
          output = (output.astype(np.float32) - z) * s
      top = np.argsort(output)[::-1][:top_k]
      print(f"Top-{top_k} predictions for {image_path}:")
      for i, idx in enumerate(top, 1):
          print(f"  #{i}  taxon_id={idx}  confidence={output[idx]:.4f}")


  def main():
      p = argparse.ArgumentParser()
      p.add_argument("--model", required=True)
      p.add_argument("--image", required=True)
      p.add_argument("--top_k", type=int, default=5)
      args = p.parse_args()
      if not Path(args.model).exists(): print(f"Model not found: {args.model}"); return 1
      if not Path(args.image).exists(): print(f"Image not found: {args.image}"); return 1
      run(args.model, args.image, args.top_k)

  if __name__ == "__main__":
      raise SystemExit(main())
  