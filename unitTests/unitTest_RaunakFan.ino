//written by Raunak with help from Joseph , edited to accomadate the altitude factor to make testing realistic.
#include <Arduino.h>

uint8_t fan = 9;    // Fan pin
uint8_t rpmPin = 2; // RPM pin

volatile int count = 0; // RPM count
unsigned long lastMillis = 0;

uint16_t lower[] = {0, 100, 280, 490, 670, 850, 1000, 1180, 1330, 1450, 1620};    // Lower bounds (expected - 80)
uint32_t upper[] = {10, 260, 440, 650, 830, 1030, 1160, 1340, 1490, 1630, 2500};  // Upper bounds (expected + 80)

void setup() {
    Serial.begin(9600);
    pinMode(fan, OUTPUT);
    pinMode(rpmPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(rpmPin), countRPM, RISING);
    analogWrite(fan, 0); // Start with the fan off
}

void loop() {
    uint8_t percent = 0; // Speed percentage
    for (int i = 0; i < 12; i++) { // Increased iterations to include the 100% duty cycle
        uint8_t speed = map(percent, 0, 100, 0, 255); // Convert percent to PWM value
        analogWrite(fan, speed); // Set fan speed
        delay(5000); // 5 second delay to stabilize

        // report RPM
        uint16_t measuredRPM = reportRPM();
        if (measuredRPM >= lower[i] && measuredRPM <= upper[i]) {
            Serial.println("Test passed");
        } else {
            Serial.println("Test failed");
        }
        
        // Increase speed percentage
        if (percent <= 100) { // While percent < 100
            percent += 10; // Increase by 10%
        } else {
            percent = 0; // Reset to 0 if at 100
        }
    }
    
    analogWrite(fan, 0); // Turn off fan 
    while(true); // Stop
}

void countRPM() {
    count++;
}

uint16_t reportRPM() {
    uint16_t rpm = count * 30;  
    return rpm; 
}
