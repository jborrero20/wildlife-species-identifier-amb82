#include "inference_engine.h"
  #include <NNBasicBlock.h>

  static NNBasicBlock nn;

  bool InferenceEngine::loadModel(const char* modelPath) {
    nn.modelPath   = modelPath;
    nn.imageWidth  = 320;
    nn.imageHeight = 320;
    nn.inputCount  = 1;
    if (nn.begin() != 0) return false;
    _loaded = true;
    return true;
  }

  int InferenceEngine::infer(const uint8_t* imageData, size_t imageSize,
                              InferenceResult* results, int topK) {
    if (!_loaded) return 0;
    nn.setInput(imageData, imageSize);
    nn.run();

    float* output    = (float*)nn.getOutput(0);
    int    numClasses = nn.getOutputSize(0) / sizeof(float);
    int    filled    = 0;
    bool   used[numClasses];
    memset(used, 0, sizeof(used));

    for (int k = 0; k < topK; k++) {
      float best = -1.0f; int bestIdx = -1;
      for (int i = 0; i < numClasses; i++) {
        if (!used[i] && output[i] > best) { best = output[i]; bestIdx = i; }
      }
      if (bestIdx < 0) break;
      used[bestIdx] = true;
      results[k].confidence = best;
      results[k].taxon_id   = bestIdx;
      snprintf(results[k].label, sizeof(results[k].label), "taxon_%d", bestIdx);
      filled++;
    }
    return filled;
  }

  void InferenceEngine::unload() {
    nn.end();
    _loaded = false;
  }
  