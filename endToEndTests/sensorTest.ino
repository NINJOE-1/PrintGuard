#include <Wire.h>
#define SLAVE_ADDRESS 0x09       // I2C address for Arduino

int temp[8] = {29, 30, 31, 32, 33, 34, 35, 36};
uint8_t i = 0;

void setup(){
  Wire.begin(SLAVE_ADDRESS);
  // Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}
void loop() {
  // Everything happens in the interrupts
}
// Handle reception of incoming I2C data
/*
void receiveData(int byteCount) {
  while (Wire.available()) {
    i2cData = Wire.read();
    if (i2cData == 1) {
  
    }
  }
}
*/
// Handle request to send I2C data
void sendData() { 
  Wire.write(temp[i]);
  i++;
}