#pragma once
  #include <Arduino.h>
  #include "VideoStream.h"

  class CameraCapture {
  public:
    bool begin(int width, int height);
    bool capture(uint8_t** buffer, size_t* size);
    void release();
  private:
    int  _width, _height;
    bool _initialized = false;
  };
  