#include "camera_capture.h"

  bool CameraCapture::begin(int width, int height) {
    _width  = width;
    _height = height;
    VideoSetting config(VIDEO_FHD, CAM_FPS, VIDEO_JPEG, 1);
    Camera.configVideoChannel(CHANNEL0, config);
    Camera.videoInit();
    Camera.channelBegin(CHANNEL0);
    _initialized = true;
    return true;
  }

  bool CameraCapture::capture(uint8_t** buffer, size_t* size) {
    if (!_initialized) return false;
    CameraImage img = Camera.getImage(CHANNEL0, _width, _height);
    if (!img.isValid()) return false;
    *buffer = img.getData();
    *size   = img.getLen();
    return true;
  }

  void CameraCapture::release() {
    Camera.channelEnd(CHANNEL0);
    _initialized = false;
  }
  