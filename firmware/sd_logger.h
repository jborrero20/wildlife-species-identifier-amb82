#pragma once
  #include <Arduino.h>
  #include <SD.h>

  class SDLogger {
  public:
    bool begin(int csPin = 10);
    void log(const char* species, float confidence, int taxonId, unsigned long ts);
    void flush();
  private:
    bool _ready = false;
    File _logFile;
    char _filename[40];
  };
  