#!/usr/bin/env python3
  """
  generate_stub_model.py
  Create a minimal INT8 TFLite model for CI validation without needing
  the full SpeciesNet weights (~100 MB).
  """
  import numpy as np
  import tensorflow as tf
  from pathlib import Path

  def build_stub(input_shape=(1, 320, 320, 3), num_classes=1000):
      inp = tf.keras.Input(shape=input_shape[1:], name="image")
      x   = tf.keras.layers.GlobalAveragePooling2D()(inp)
      out = tf.keras.layers.Dense(num_classes, activation="softmax", name="predictions")(x)
      return tf.keras.Model(inp, out)

  def main():
      model = build_stub()

      converter = tf.lite.TFLiteConverter.from_keras_model(model)
      converter.optimizations = [tf.lite.Optimize.DEFAULT]

      def rep_data():
          for _ in range(10):
              yield [np.random.uniform(0, 1, (1, 320, 320, 3)).astype(np.float32)]

      converter.representative_dataset = rep_data
      converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
      converter.inference_input_type  = tf.int8
      converter.inference_output_type = tf.int8

      tflite_model = converter.convert()

      out = Path("model/stub_int8.tflite")
      out.parent.mkdir(parents=True, exist_ok=True)
      out.write_bytes(tflite_model)
      print(f"Stub model saved: {out}  ({len(tflite_model)/1024:.1f} KB)")

  if __name__ == "__main__":
      main()
  