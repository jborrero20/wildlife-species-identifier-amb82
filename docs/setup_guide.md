# Setup Guide — Wildlife Species Identifier on AMB82-Mini

  ## Prerequisites

  - Arduino IDE 2.x
  - AMB82-Mini board package installed
  - Python 3.9+
  - AMB82-Mini + camera module + MicroSD card (FAT32)

  ## Step 1 — Install AMB82-Mini Board Support

  1. Arduino IDE → Preferences → Additional Boards Manager URLs:
     `https://github.com/ambiot/ambpro2_arduino/raw/main/Arduino_package/package_realtek_amebapro2_early_index.json`
  2. Tools → Board Manager → search "AMB82-Mini" → Install

  ## Step 2 — Prepare SpeciesNet Model

  ```bash
  pip install -r requirements.txt

  # Download SpeciesNet SavedModel, then:
  python model/convert_to_tflite.py --output model/speciesnet_int8.tflite
  python model/validate_model.py --model model/speciesnet_int8.tflite --image your_test.jpg
  ```

  Copy `speciesnet_int8.tflite` to the root of your MicroSD card.

  ## Step 3 — Flash Firmware

  1. Connect AMB82-Mini via USB-C
  2. Open `firmware/amb82_speciesnet.ino` in Arduino IDE
  3. **Tools → Board → AMB82-Mini**
  4. Click Upload

  ## Step 4 — Monitor Detections

  ```bash
  python host_tools/serial_monitor.py --port /dev/ttyUSB0
  ```

  ## Step 5 — Visualize Logged Data

  After collecting detections on the SD card:

  ```bash
  python host_tools/data_visualizer.py --csv DETECTIONS/log_00012345.csv
  ```

  ## Wiring (GPS module — optional)

  | NEO-6M Pin | AMB82-Mini Pin |
  |------------|----------------|
  | VCC        | 3.3V           |
  | GND        | GND            |
  | TX         | UART2 RX       |
  | RX         | UART2 TX       |
  