# Wildlife Species Identifier — SpeciesNet on AMB82-Mini
  > **Track:** Edge AI / Conservation Tech | **Difficulty:** Advanced

  A real-time wildlife species identification system running Google's [SpeciesNet](https://github.com/google/speciesnet) model on the [Realtek AMB82-Mini](https://www.amebaiot.com/en/amebapro2/) embedded AI camera board. Designed for low-power, offline deployment in field conservation settings.

  ---

  ## Overview

  This project captures images from the AMB82-Mini's onboard camera, runs SpeciesNet inference locally, and logs identified species with confidence scores — all without cloud connectivity.

  ## Features

  - Real-time species classification using SpeciesNet (TFLite INT8 quantized)
  - Onboard JPEG image capture via AMB82-Mini camera module
  - Local inference with no internet required
  - SD card logging of detections with timestamps
  - Optional Wi-Fi sync to conservation database endpoint
  - Serial monitor output for debugging

  ## Hardware Requirements

  | Component | Details |
  |-----------|---------|
  | AMB82-Mini | Realtek RTL8735B, dual-core ARM, built-in NPU |
  | Camera Module | OV5647 or GC2053 (AMB82-Mini compatible) |
  | MicroSD Card | FAT32 formatted, for local data logging |
  | GPS Module (optional) | UART NEO-6M |
  | LiPo Battery | 3.7V, 2000mAh+ for field use |

  ## Software Architecture

  ```
  ┌─────────────────────────────────────────┐
  │             AMB82-Mini                  │
  │  ┌─────────┐    ┌──────────────────┐   │
  │  │ Camera  │───▶│  Image Capture   │   │
  │  └─────────┘    └────────┬─────────┘   │
  │                  ┌───────▼──────────┐  │
  │                  │  Pre-processing  │  │
  │                  └───────┬──────────┘  │
  │                  ┌───────▼──────────┐  │
  │                  │  SpeciesNet NPU  │  │
  │                  └───────┬──────────┘  │
  │           ┌──────────────▼──────┐      │
  │           │   Post-processing   │      │
  │           └──┬──────────────┬───┘      │
  │        ┌─────▼───┐   ┌──────▼──────┐  │
  │        │  Serial │   │  SD Logger  │  │
  │        └─────────┘   └─────────────┘  │
  └─────────────────────────────────────────┘
  ```

  ## Project Structure

  ```
  wildlife-species-identifier-amb82/
  ├── firmware/
  │   ├── amb82_speciesnet.ino      # Main Arduino sketch
  │   ├── camera_capture.cpp/.h     # Camera driver wrapper
  │   ├── inference_engine.cpp/.h   # TFLite NPU inference
  │   └── sd_logger.cpp/.h          # SD card CSV logging
  ├── model/
  │   ├── convert_to_tflite.py      # SpeciesNet → TFLite INT8 conversion
  │   └── validate_model.py         # PC-side model validation
  ├── host_tools/
  │   ├── serial_monitor.py         # Real-time serial output viewer
  │   └── data_visualizer.py        # Plot detection logs
  ├── docs/
  │   └── setup_guide.md
  ├── config.yaml
  ├── requirements.txt
  ├── .gitignore
  └── README.md
  ```

  ## Getting Started

  ### 1. Model Preparation (PC)

  ```bash
  git clone https://github.com/jborrero20/wildlife-species-identifier-amb82.git
  cd wildlife-species-identifier-amb82
  pip install -r requirements.txt
  python model/convert_to_tflite.py --output model/speciesnet_int8.tflite
  python model/validate_model.py --model model/speciesnet_int8.tflite
  ```

  ### 2. Flash the Firmware

  1. Install Arduino IDE with AMB82-Mini board support
  2. Copy `speciesnet_int8.tflite` to the MicroSD card root
  3. Open `firmware/amb82_speciesnet.ino`
  4. Select **Tools → Board → AMB82-Mini** and upload

  ### 3. Monitor Output

  ```bash
  python host_tools/serial_monitor.py --port /dev/ttyUSB0
  ```

  ## Configuration

  Edit `config.yaml` to adjust thresholds, logging, and Wi-Fi sync settings.

  ## Power Consumption

  | Mode | Current |
  |------|---------|
  | Capture + Inference | ~280 mA |
  | Idle / sleep | ~8 mA |
  | Wi-Fi sync active | ~380 mA |

  ## License

  MIT — see [LICENSE](LICENSE)

  ## References

  - [SpeciesNet by Google](https://github.com/google/speciesnet)
  - [AMB82-Mini Arduino SDK](https://github.com/ambiot/ambpro2_arduino)
  - [TFLite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers)
  