#include <HardwareSerial.h>

// Define pins
#define RADAR_RX 14  // ESP32 receives data from radar TX
#define RADAR_TX 16  // ESP32 transmits data to radar RX

// UART2 object
HardwareSerial RadarSerial(2);

void setup() {
  // Start Serial (USB to PC)
  Serial.begin(256000);
  while (!Serial); // Wait for Serial Monitor

  Serial.println("ESP32-CAM Serial Bridge Started");

  // Start UART2 to radar
  RadarSerial.begin(256000, SERIAL_8N1, RADAR_RX, RADAR_TX);
}

void loop() {
  // Forward data from PC (USB) to Radar
  while (Serial.available()) {
    char incoming = Serial.read();
    RadarSerial.write(incoming);
  }

  // Forward data from Radar to PC (USB)
  while (RadarSerial.available()) {
    char incoming = RadarSerial.read();
    Serial.write(incoming);
  }
}
