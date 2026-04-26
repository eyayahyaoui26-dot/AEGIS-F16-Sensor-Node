# ============================================
#   AEGIS BRIDGE v1.1 — ESP32 (SANS BMP180)
#   Port: COM3 | Baud: 115200
# ============================================

import serial
import json
import threading
import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── CONFIG ──────────────────────────────────
SERIAL_PORT = 'COM3'  # Thabbet dima mel Device Manager
BAUD_RATE = 115200 
# ────────────────────────────────────────────

# Houni na7ina el Altitude wel Pressure khater nahit el BMP180
sensor_data = {
    "temp": 0, 
    "humidity": 0,
    "gForce": 0, 
    "maxG": 0,
    "flightSecs": 0,
    "connected": False
}

# ── SERIAL READER (Thread) ──────────────────
def read_esp32():
    global sensor_data
    print(f"[AEGIS] Attempting connection on {SERIAL_PORT}...")
    
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"[AEGIS] ✓ Connected to ESP32 on {SERIAL_PORT}")
            sensor_data["connected"] = True
            
            buffer = ""
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not line: continue

                    # Debug bech tchouf el data elli jaya mel ESP32
                    print(f"[RAW DATA] {line}")

                    # Début du JSON
                    if line == '{':
                        buffer = '{'
                    # Fin du JSON
                    elif line == '}':
                        buffer += '}'
                        try:
                            parsed = json.loads(buffer)
                            # On met à jour les données mrigel
                            sensor_data.update(parsed)
                            sensor_data["connected"] = True
                        except Exception as e:
                            print(f"[ERROR] JSON Decode Error: {e}")
                        buffer = ""
                    # Accumulation des lignes entre { et }
                    else:
                        if buffer.startswith('{'):
                            buffer += line
                            
                time.sleep(0.01)

        except Exception as e:
            print(f"[AEGIS] ✗ Connection Error: {e}")
            sensor_data["connected"] = False
            print("[AEGIS] Retrying in 3 seconds...")
            time.sleep(3)

# ── FLASK ROUTES ────────────────────────────
@app.route('/data')
def get_data():
    return jsonify(sensor_data)

# ── MAIN ─────────────────────────────────────
if __name__ == '__main__':
    # 1. Khaddem el-khit elli ya7ki m3a el-ESP32
    serial_thread = threading.Thread(target=read_esp32, daemon=True)
    serial_thread.start()

    # 2. Khaddem el-Server mte3 el-Dashboard
    print("[AEGIS] Bridge is running on http://127.0.0.1:5000/data")
    app.run(port=5000, debug=False, use_reloader=False)