#pragma once
  #include <Arduino.h>

  struct InferenceResult {
    char  label[128];
    int   taxon_id;
    float confidence;
  };

  class InferenceEngine {
  public:
    bool loadModel(const char* modelPath);
    int  infer(const uint8_t* imageData, size_t imageSize,
               InferenceResult* results, int topK);
    void unload();
  private:
    bool _loaded = false;
  };
  