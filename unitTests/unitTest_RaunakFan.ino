//written by Raunak Soi
#include <Arduino.h>

const uint8_t fan = 9;    // Fan pin
const uint8_t rpmPin = 2; // RPM pin
const unsigned long measurementWindow = 1000; // 1 second measurement window, declared as a constant

volatile int count = 0; // RPM count

const uint16_t lower[] = {0, 100, 280, 490, 670, 850, 1000, 1180, 1330, 1450, 1620};    // Lower bounds (expected - 80)
const uint32_t upper[] = {10, 260, 440, 650, 830, 1030, 1160, 1340, 1490, 1630, 2500};  // Upper bounds (expected + 80)

// added some counters for passed and failed tests
int passedTests = 0;
int failedTests = 0;

void setup() {
    Serial.begin(9600);
    pinMode(fan, OUTPUT);
    pinMode(rpmPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(rpmPin), countRPM, RISING);
    analogWrite(fan, 0); // Starting with the fan off
}

void loop() {
    for (int i = 0; i < 11; i++) {
        uint8_t percent = i * 10; // Calculate percentage
        uint8_t speed = map(percent, 0, 100, 0, 255); // Convert percent to PWM value
        analogWrite(fan, speed); // Setting fan speed
        delay(5000); // 5 second delay to stabilize
        
        count = 0; // Reset count after the fan has stabilized
        unsigned long measurementStartTime = millis();

        while (millis() - measurementStartTime < measurementWindow) {
            // CountRPM function is active and counting the RPM.
        }

        uint16_t measuredRPM = reportRPM();
        Serial.print("Speed: "); Serial.print(percent); Serial.print("%, RPM: "); Serial.println(measuredRPM); // Print the current RPM

        if (measuredRPM >= lower[i] && measuredRPM <= upper[i]) {
            Serial.println("Test passed");
            passedTests++; 
        } else {
            Serial.println("Test failed");
            failedTests++;
        }
    }
    
    // Print summary of test results
    Serial.print("Testing complete. Passed: ");
    Serial.print(passedTests);
    Serial.print(", Failed: ");
    Serial.println(failedTests);
    
    analogWrite(fan, 0); // Turn off fan 
    while(true); // Stopping loop to prevent re-running tests automatically
}

void countRPM() {
    count++; // Increments on each rising edge
}

uint16_t reportRPM() {
    uint16_t rpm = count * 30;
    return rpm;
}
