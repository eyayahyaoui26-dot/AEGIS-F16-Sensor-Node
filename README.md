   AEGIS F16 Sensor Node

[AEGIS Banner]
> **Real-time F16 Mission Control System** — ESP32 sensor data streamed live to AEGIS Dashboard
> 
 Project Photos
| Hardware Setup | Serial Monitor | Dashboard |
|---|---|---|
| ![Hardware] | ![Serial] | ![Dashboard] |


  Hardware

![Wiring]

| Component | Role |
|---|---|
| **ESP32 NodeMCU** | Main controller |
| **DHT22** | Temperature + Humidity |
| **BMP180** | Pressure + Altitude |
| **MPU6050** | G-Force + Gyroscope |



 Wiring

![Wiring Diagram]

| Sensor | ESP32 Pin | Wire Color |
|---|---|---|
| DHT22 VCC | 3.3V |  Red |
| DHT22 DATA | GPIO 4 |  Yellow |
| DHT22 GND | GND |  Black |
| BMP180 SDA | GPIO 21 |  Green |
| BMP180 SCL | GPIO 22 |  Blue |
| BMP180 VCC | 3.3V | Red |
| BMP180 GND | GND |  Black |
| MPU6050 SDA | GPIO 21 |  Green |
| MPU6050 SCL | GPIO 22 |  Blue |
| MPU6050 VCC | 3.3V |  Red |
| MPU6050 GND | GND |  Black |

>  BMP180 and MPU6050 share the same SDA/SCL — this is normal for I2C !



 Libraries Required

Install these in **Arduino IDE → Manage Libraries** :

| Library | Author |
|---|---|
| `DHT sensor library` | Adafruit |
| `Adafruit BMP085 Library` | Adafruit |
| `MPU6050` | Electronic Cats |



 How to Run

 1. Upload Arduino Code
- Open `sketch_apr23a/sketch_apr23a.ino` in Arduino IDE
- Select board : **ESP32 Dev Module**
- Select port : **COM3**
- Click **Upload**

 2. Verify in Serial Monitor
Open Serial Monitor at **115200 baud** — you should see :
~~~~
============================
   AEGIS SENSOR NODE v3.0  
============================
[DHT22]   OK
[BMP180]  OK
[MPU6050] OK
[BATTERY] Mode simulation active
[AEGIS]   TOUS SYSTEMES EN LIGNE
~~~~

3. Launch Python Bridge
 bash
pip install pyserial
python aegis_bridge.py


You should see :

[AEGIS] ESP32 connecte sur COM3
[SENSOR] T:24.5C | G:1.02G | Alt:12.3m | B:93.9%


 4. Open Dashboard

http://localhost:5000/sensors




📡 JSON Data Output

```json
{
  "temp": 24.5,
  "humidity": 58.2,
  "pressure": 1013.45,
  "altitude": 12.3,
  "gForce": 1.02,
  "gX": 0.01,
  "gY": 0.02,
  "gZ": 1.00,
  "gyroX": 0.1,
  "gyroY": 0.2,
  "gyroZ": 0.0,
  "battery": 93.5,
  "maxG": 1.02,
  "flightMins": 0,
  "flightSecs": 45,
  "connected": true
}
```

---

 AEGIS Alerts

| Alert | Condition |
|---|---|
| 🔴 CRITIQUE G-FORCE | G > 7G — Blackout risk ! |
| 🟡 WARNING G-FORCE | G > 5G — High G-force |
| 🔴 CRITIQUE BATTERY | Battery < 20% |
| 🟡 WARNING BATTERY | Battery < 40% |
| 🟡 WARNING TEMP | Temp > 40°C |
| 🟡 WARNING PRESSURE | Pressure < 1000 hPa |

---

📁 Project Structure

```
AEGIS-F16-Sensor-Node/
│
├── sketch_apr23a/
│   └── sketch_apr23a.ino     ← ESP32 Arduino code
│
├── aegis_bridge.py           ← Python Serial → HTTP bridge
├── aegis_final.html          ← AEGIS Dashboard
├── photos/                   ← Project photos
└── README.md
```

---

  Author

**eyayahyaoui26-dot**
- GitHub : [@eyayahyaoui26-dot](https://github.com/eyayahyaoui26-dot)

---

   License
MIT License — Free to use and modify
