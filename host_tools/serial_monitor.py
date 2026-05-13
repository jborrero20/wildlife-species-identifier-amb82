#!/usr/bin/env python3
  """
  serial_monitor.py — Real-time AMB82-Mini detection viewer.

  Usage:
      python host_tools/serial_monitor.py --port /dev/ttyUSB0
  """
  import argparse, re, sys
  from datetime import datetime

  try:
      import serial
  except ImportError:
      print("Install pyserial: pip install pyserial"); sys.exit(1)

  DETECT_RE = re.compile(r"#(\d+)\s+(.+?)\s{2,}([\d.]+)%")

  def monitor(port, baud=115200):
      print(f"Connecting to {port} @ {baud} baud...")
      with serial.Serial(port, baud, timeout=1) as ser:
          print("Connected. Listening for detections (Ctrl+C to stop)\n")
          try:
              while True:
                  line = ser.readline().decode("utf-8", errors="replace").strip()
                  if not line: continue
                  m = DETECT_RE.search(line)
                  if m:
                      ts = datetime.now().strftime("%H:%M:%S")
                      rank, species, conf = m.group(1), m.group(2).strip(), m.group(3)
                      print(f"[{ts}] #{rank}  {species:<45}  {conf}%")
                  else:
                      print(f"[DBG] {line}")
          except KeyboardInterrupt:
              print("\nMonitor stopped.")

  def main():
      p = argparse.ArgumentParser()
      p.add_argument("--port", default="/dev/ttyUSB0")
      p.add_argument("--baud", type=int, default=115200)
      monitor(**vars(p.parse_args()))

  if __name__ == "__main__":
      main()
  