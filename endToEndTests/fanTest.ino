#include <Wire.h>
#define ADDRESS 0x08
#define RED 4
#define GREEN 6
#define BLUE 7

uint8_t data;

void setup(){
  Wire.begin(ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
}

void loop() {}

void receiveData(int byteCount) {
  while (Wire.available()) {
    data = Wire.read();
    if (data < 31) {
      digitalWrite(RED, LOW);
      digitalWrite(GREEN, LOW);
      digitalWrite(BLUE, HIGH);
    } else if (data >= 31 && data < 34) {
      digitalWrite(RED, LOW);
      digitalWrite(GREEN, HIGH);
      digitalWrite(BLUE, LOW);
    } else if (data >= 34) {
      digitalWrite(RED, HIGH);
      digitalWrite(GREEN, LOW);
      digitalWrite(BLUE, LOW);
    }
  }
}

void sendData() {
  if (data < 31) {
    Wire.write(0);
  } else if (data > 31 && data < 34) {
    Wire.write(128);
  } else if (data >= 34) {
    Wire.write(255);
  }
}