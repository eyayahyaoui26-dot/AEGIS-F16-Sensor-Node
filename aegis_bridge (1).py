# ============================================
#   AEGIS BRIDGE v1.0 — ESP32 VERSION
#   Port: COM3 | Baud: 115200
# ============================================

import serial
import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── CONFIG ──────────────────────────────────
SERIAL_PORT = 'COM3'        # Thabbet mel Device Manager dima
BAUD_RATE   = 115200        # ESP32 dima 115200
SERVER_PORT = 5000
# ────────────────────────────────────────────

sensor_data = {
    "temp": 0.0, "humidity": 0.0, "pressure": 1013.25,
    "altitude": 0.0, "gForce": 1.0, "battery": 100, "connected": False
}

# ── HTTP SERVER ──────────────────────────────
class AEGISHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/sensors':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(sensor_data).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass # Pour garder le terminal propre

# ── SERIAL READER ────────────────────────────
def read_esp32():
    global sensor_data
    print(f"[AEGIS] Attempting connection on {SERIAL_PORT}...")

    while True:
        try:
            # On ouvre le port série
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            print(f"[AEGIS] ✓ ESP32 Connected on {SERIAL_PORT}")
            sensor_data["connected"] = True
            
            buffer = ""
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not line: continue

                    # Debug: affiche ce que l'ESP32 envoie réellement
                    print(f"[RAW DATA] {line}")

                    # Gestion du JSON (reconstruction si envoyé ligne par ligne)
                    if line == '{':
                        buffer = '{'
                    elif line == '}':
                        buffer += '}'
                        try:
                            parsed = json.loads(buffer)
                            sensor_data.update(parsed)
                            sensor_data["connected"] = True
                            print(f"[SUCCESS] Data Updated")
                        except Exception as e:
                            print(f"[ERROR] JSON: {e}")
                        buffer = ""
                    else:
                        if buffer.startswith('{'):
                            buffer += line
                time.sleep(0.01) # Petit repos pour le CPU

        except serial.SerialException as e:
            print(f"[AEGIS] ✗ Connection lost: {e}")
            sensor_data["connected"] = False
            time.sleep(3) # Attendre avant de réessayer
        except Exception as e:
            print(f"[AEGIS] Critical Error: {e}")
            time.sleep(3)

# ── MAIN ─────────────────────────────────────
if __name__ == '__main__':
    print("============================================")
    print("   AEGIS BRIDGE v1.0 — ESP32 READY         ")
    print("============================================")

    # Lancement du thread série
    serial_thread = threading.Thread(target=read_esp32, daemon=True)
    serial_thread.start()

    print(f"[AEGIS] Server: http://localhost:{SERVER_PORT}/sensors")
    
    try:
        server = HTTPServer(('0.0.0.0', SERVER_PORT), AEGISHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[AEGIS] Bridge shutting down...")