#include <Wire.h>
#include <DHT.h>
#include <MPU6050.h>

// ---------- 1. CONFIGURATION DES PINS ----------
// Bus I2C pour MPU6050 sur les pins 21 et 22
TwoWire I2C_MPU = TwoWire(0); 

// Configuration DHT22 sur le Pin 4
#define DHTPIN  4
#define DHTTYPE DHT22

// ---------- 2. INSTANCES ----------
DHT dht(DHTPIN, DHTTYPE);
MPU6050 mpu(0x68, &I2C_MPU); 

unsigned long lastRead = 0;
unsigned long startTime = 0;
float maxG = 0.0;

void setup() {
  Serial.begin(115200);
  delay(1000); // Temps de stabilisation

  // Initialisation I2C et DHT
  I2C_MPU.begin(21, 22, 400000);
  dht.begin();
  
  startTime = millis();

  Serial.println("\n=== CONFIGURATION AEGIS (SANS BMP) ===");

  // Initialisation MPU6050
  mpu.initialize();
  if (mpu.testConnection()) {
    Serial.println("[MPU6050] OK : Connecté sur 21/22");
  } else {
    Serial.println("[MPU6050] ERREUR : Verifiez le cablage");
  }
  
  Serial.println("[DHT22] Initialisé sur Pin 4");
}

void loop() {
  // Lecture toutes les 2 secondes pour ne pas bloquer le capteur
  if (millis() - lastRead >= 2000) {
    lastRead = millis();

    // 1. Lecture Temperature et Humidité
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // 2. Lecture MPU6050 (Accélération)
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // Calcul de la Force G
    float gTotal = sqrt(pow(ax/16384.0, 2) + pow(ay/16384.0, 2) + pow(az/16384.0, 2));
    if (gTotal > maxG) maxG = gTotal;

    unsigned long flightSecs = (millis() - startTime) / 1000;

    // Output JSON pour Python (AEGIS MCS)
    Serial.println("{");
    Serial.print("  \"temp\":"); Serial.print(t, 1); Serial.println(",");
    Serial.print("  \"humidity\":"); Serial.print(h, 1); Serial.println(",");
    Serial.print("  \"gForce\":"); Serial.print(gTotal, 2); Serial.println(",");
    Serial.print("  \"maxG\":"); Serial.print(maxG, 2); Serial.println(",");
    Serial.print("  \"flightSecs\":"); Serial.print(flightSecs);
    Serial.println("\n}");
    Serial.println("---");
  }
}