# ============================================
#   AEGIS BRIDGE v1.0 — ESP32 VERSION
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
SERIAL_PORT = 'COM3'  # Thabbet mel-Device Manager dima
BAUD_RATE = 115200    # ESP32 dima 115200
# ────────────────────────────────────────────

sensor_data = {
    "temp": 0, 
    "gForce": 0, 
    "altitude": 0, 
    "battery": 0, 
    "connected": False
}

# ── SERIAL READER (Thread) ──────────────────
def read_esp32():
    global sensor_data
    print(f"[AEGIS] Attempting connection on {SERIAL_PORT}...")
    
    while True:
        try:
            # On ouvre le port série
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"[AEGIS] ✓ Connected to ESP32 on {SERIAL_PORT}")
            sensor_data["connected"] = True
            
            buffer = ""
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not line: continue

                    # Debug: taw tchouf el data el-7aya houni
                    print(f"[RAW DATA] {line}")

                    if line == '{':
                        buffer = '{'
                    elif line == '}':
                        buffer += '}'
                        try:
                            parsed = json.loads(buffer)
                            sensor_data.update(parsed)
                            sensor_data["connected"] = True
                        except Exception as e:
                            print(f"[ERROR] JSON Decode: {e}")
                        buffer = ""
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
    # 1. Khaddem el-khit elli ya7ki m3a el-Arduino
    serial_thread = threading.Thread(target=read_esp32, daemon=True)
    serial_thread.start()

    # 2. Khaddem el-Server mte3 el-Dashboard
    print("[AEGIS] Bridge is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=False, use_reloader=False)