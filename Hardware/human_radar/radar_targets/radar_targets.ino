#define RX_PIN 14
#define TX_PIN 16
#define BAUD_RATE 256000
 
// Variables
uint8_t RX_BUF[64] = {0};
uint8_t RX_count = 0;
uint8_t RX_temp = 0;
 
// Target details
int16_t target1_x = 0, target1_y = 0;
int16_t target1_speed = 0;
uint16_t target1_distance_res = 0;
 
int16_t target2_x = 0, target2_y = 0;
int16_t target2_speed = 0;
uint16_t target2_distance_res = 0;
 
int16_t target3_x = 0, target3_y = 0;
int16_t target3_speed = 0;
uint16_t target3_distance_res = 0;
 
 
// Single-Target Detection Command
uint8_t Single_Target_Detection_CMD[12] = {0xFD, 0xFC, 0xFB, 0xFA, 0x02, 0x00, 0x80, 0x00, 0x04, 0x03, 0x02, 0x01};
 
// Multi-Target Detection Command
uint8_t Multi_Target_Detection_CMD[12] = {0xFD, 0xFC, 0xFB, 0xFA, 0x02, 0x00, 0x90, 0x00, 0x04, 0x03, 0x02, 0x01};
 
void setup() {
    Serial.begin(115200);                  // Debugging
    Serial1.begin(BAUD_RATE, SERIAL_8N1, RX_PIN, TX_PIN);
    Serial1.setRxBufferSize(64);           // Set buffer size
    Serial.println("RD-03D Radar Module Initialized");
 
    // Send multi-target detection command
    Serial1.write(Multi_Target_Detection_CMD, sizeof(Multi_Target_Detection_CMD));
    delay(200);
    Serial.println("Multi-target detection mode activated.");
 
    RX_count = 0;
    Serial1.flush();
}
 
void processRadarData() {
 
   // output data
   //printBuffer();
 
   /* RX_BUF: 0xAA 0xFF 0x03 0x00                   Header
    *  0x05 0x01 0x19 0x82 0x00 0x00 0x68 0x01      target1
    *  0xE3 0x81 0x33 0x88 0x20 0x80 0x68 0x01      target2
    *  0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00      target3
    *  0x55 0xCC
  */
 
  
    if (RX_count >= 32) {
        // Extract data for Target 1
        target1_x = (RX_BUF[4] | (RX_BUF[5] << 8)) - 0x200;
        target1_y = (RX_BUF[6] | (RX_BUF[7] << 8)) - 0x8000;
        target1_speed = (RX_BUF[8] | (RX_BUF[9] << 8)) - 0x10;
        target1_distance_res = (RX_BUF[10] | (RX_BUF[11] << 8));
        float target1_distance = sqrt(pow(target1_x, 2) + pow(target1_y, 2));
        float target1_angle = atan2(target1_y, target1_x) * 180.0 / PI;
 
        Serial.print("Target 1 - Distance: ");
        Serial.print(target1_distance / 10.0);
        Serial.print(" cm, Angle: ");
        Serial.print(target1_angle);
        Serial.print(" degrees, X: ");
        Serial.print(target1_x);
        Serial.print(" mm, Y: ");
        Serial.print(target1_y);
        Serial.print(" mm, Speed: ");
        Serial.print(target1_speed);
        Serial.print(" cm/s, Distance Resolution: ");
        Serial.print(target1_distance_res);
        Serial.println(" mm");
 
        // Extract data for Target 2
        target2_x = (RX_BUF[12] | (RX_BUF[13] << 8)) - 0x200;
        target2_y = (RX_BUF[14] | (RX_BUF[15] << 8)) - 0x8000;
        target2_speed = (RX_BUF[16] | (RX_BUF[17] << 8)) - 0x10;
        target2_distance_res = (RX_BUF[18] | (RX_BUF[19] << 8));
        float target2_distance = sqrt(pow(target2_x, 2) + pow(target2_y, 2));
        float target2_angle = atan2(target2_y, target2_x) * 180.0 / PI;
 
        Serial.print("Target 2 - Distance: ");
        Serial.print(target2_distance / 10.0);
        Serial.print(" cm, Angle: ");
        Serial.print(target2_angle);
        Serial.print(" degrees, X: ");
        Serial.print(target2_x);
        Serial.print(" mm, Y: ");
        Serial.print(target2_y);
        Serial.print(" mm, Speed: ");
        Serial.print(target2_speed);
        Serial.print(" cm/s, Distance Resolution: ");
        Serial.print(target2_distance_res);
        Serial.println(" mm");
 
        // Extract data for Target 3
        target3_x = (RX_BUF[20] | (RX_BUF[21] << 8)) - 0x200;
        target3_y = (RX_BUF[22] | (RX_BUF[23] << 8)) - 0x8000;
        target3_speed = (RX_BUF[24] | (RX_BUF[25] << 8)) - 0x10;
        target3_distance_res = (RX_BUF[26] | (RX_BUF[27] << 8));
        float target3_distance = sqrt(pow(target3_x, 2) + pow(target3_y, 2));
        float target3_angle = atan2(target3_y, target3_x) * 180.0 / PI;
 
        Serial.print("Target 3 - Distance: ");
        Serial.print(target3_distance / 10.0);
        Serial.print(" cm, Angle: ");
        Serial.print(target3_angle);
        Serial.print(" degrees, X: ");
        Serial.print(target3_x);
        Serial.print(" mm, Y: ");
        Serial.print(target3_y);
        Serial.print(" mm, Speed: ");
        Serial.print(target3_speed);
        Serial.print(" cm/s, Distance Resolution: ");
        Serial.print(target3_distance_res);
        Serial.println(" mm");
 
        // Reset buffer and counter
        memset(RX_BUF, 0x00, sizeof(RX_BUF));
        RX_count = 0;
    }
}
 
void loop() {
    // Read data from Serial1
    while (Serial1.available()) {
        RX_temp = Serial1.read();
        RX_BUF[RX_count++] = RX_temp;
 
        // Prevent buffer overflow
        if (RX_count >= sizeof(RX_BUF)) {
            RX_count = sizeof(RX_BUF) - 1;
        }
 
        // Check for end of frame (0xCC, 0x55)
        if ((RX_count > 1) && (RX_BUF[RX_count - 1] == 0xCC) && (RX_BUF[RX_count - 2] == 0x55)) {
            processRadarData();
        }
    }
}
 
 
 
// Function to print buffer contents
void printBuffer() {
    Serial.print("RX_BUF: ");
    for (int i = 0; i < RX_count; i++) {
        Serial.print("0x");
        if (RX_BUF[i] < 0x10) Serial.print("0");  // Add leading zero for single-digit hex values
        Serial.print(RX_BUF[i], HEX);
        Serial.print(" ");
    }
    Serial.println();
}