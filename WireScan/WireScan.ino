#include <Wire.h>

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("\n--- SCANNER DE BUS I2C ---");

  // On teste le Bus 2 (32/33)
  TwoWire I2C_2 = TwoWire(1);
  I2C_2.begin(32, 33);

  Serial.println("Scan du Bus 2 (Pins 32/33)...");
  byte error, address;
  int nDevices = 0;

  for(address = 1; address < 127; address++ ) {
    I2C_2.beginTransmission(address);
    error = I2C_2.endTransmission();

    if (error == 0) {
      Serial.print("Dispositif trouvé à l'adresse 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    }
  }

  if (nDevices == 0) Serial.println("Aucun capteur trouvé sur 32/33.");
  else Serial.println("Scan terminé.");
}

void loop() {}