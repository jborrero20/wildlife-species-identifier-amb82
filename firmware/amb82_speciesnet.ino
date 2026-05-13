/*
   * Wildlife Species Identifier — AMB82-Mini
   * SpeciesNet TFLite Inference on Realtek RTL8735B NPU
   * Track: Edge AI / Conservation Tech | Difficulty: Advanced
   */

  #include "camera_capture.h"
  #include "inference_engine.h"
  #include "sd_logger.h"

  #define CAPTURE_INTERVAL_MS   5000
  #define CONFIDENCE_THRESHOLD  0.65f
  #define TOP_K                 3
  #define IMAGE_WIDTH           320
  #define IMAGE_HEIGHT          320

  CameraCapture  camera;
  InferenceEngine engine;
  SDLogger       logger;

  void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("=== Wildlife Species Identifier ===");
    Serial.println("  SpeciesNet on AMB82-Mini");
    Serial.println("===================================");

    if (!camera.begin(IMAGE_WIDTH, IMAGE_HEIGHT)) {
      Serial.println("[ERROR] Camera init failed. Halting.");
      while (true) delay(1000);
    }
    Serial.println("[OK] Camera initialized");

    if (!engine.loadModel("/speciesnet_int8.tflite")) {
      Serial.println("[ERROR] Model load failed. Halting.");
      while (true) delay(1000);
    }
    Serial.println("[OK] SpeciesNet model loaded");

    if (!logger.begin()) {
      Serial.println("[WARN] SD card not found — logging disabled");
    } else {
      Serial.println("[OK] SD card ready");
    }

    Serial.println("[READY] Starting detection loop...\n");
  }

  void loop() {
    uint32_t t_start = millis();

    uint8_t* imageBuffer = nullptr;
    size_t   imageSize   = 0;
    if (!camera.capture(&imageBuffer, &imageSize)) {
      Serial.println("[WARN] Capture failed, skipping frame");
      delay(CAPTURE_INTERVAL_MS);
      return;
    }

    InferenceResult results[TOP_K];
    int numResults = engine.infer(imageBuffer, imageSize, results, TOP_K);

    Serial.printf("[DETECT] %d species found (>%.0f%% confidence)\n",
                  numResults, CONFIDENCE_THRESHOLD * 100);

    for (int i = 0; i < numResults; i++) {
      if (results[i].confidence < CONFIDENCE_THRESHOLD) break;
      Serial.printf("  #%d  %-40s  %.1f%%\n",
                    i + 1, results[i].label, results[i].confidence * 100.0f);
      logger.log(results[i].label, results[i].confidence,
                 results[i].taxon_id, millis());
    }

    uint32_t elapsed = millis() - t_start;
    Serial.printf("[TIMING] Cycle: %lu ms\n\n", elapsed);
    logger.flush();

    if (elapsed < CAPTURE_INTERVAL_MS)
      delay(CAPTURE_INTERVAL_MS - elapsed);
  }
  