#include "sd_logger.h"

  bool SDLogger::begin(int csPin) {
    if (!SD.begin(csPin)) return false;
    if (!SD.exists("/DETECTIONS")) SD.mkdir("/DETECTIONS");
    snprintf(_filename, sizeof(_filename), "/DETECTIONS/log_%08lu.csv", millis());
    _logFile = SD.open(_filename, FILE_WRITE);
    if (_logFile && _logFile.size() == 0)
      _logFile.println("timestamp_ms,taxon_id,species,confidence");
    _ready = (_logFile != false);
    return _ready;
  }

  void SDLogger::log(const char* species, float confidence,
                     int taxonId, unsigned long ts) {
    if (!_ready) return;
    _logFile.printf("%lu,%d,\"%s\",%0.4f\n", ts, taxonId, species, confidence);
  }

  void SDLogger::flush() {
    if (_logFile) _logFile.flush();
  }
  