#include <Wire.h>

#define ADDRESS 0x08
#define PWMPIN 9
#define RPMPIN 2

uint8_t pwm = 0;
uint32_t count = 0;
uint8_t data [] = {0, 0};
unsigned long start_time;
uint16_t rpm;
uint8_t incoming;

void setup() {
  Wire.begin(ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  pinMode(PWMPIN, OUTPUT);
  pinMode(RPMPIN, INPUT_PULLUP);
  analogWrite(PWMPIN, pwm);
  attachInterrupt(digitalPinToInterrupt(RPMPIN), counter, RISING);
}

void loop() {
  analogWrite(PWMPIN, pwm);
}

void receiveData(int byteCount) {
  while (Wire.available()) {
    incoming = Wire.read();
    if (incoming < 31) {
      pwm = 0;
    } else if (data >= 31 && data < 34) {
      pwm = 127;
    } else {
      pwm = 255;
    }
  }
}

void sendData() {
  //count = 0;
  //start_time = millis();
  //while((millis() - start_time) < 1000) {}
  //rpm = (count * 30);
  rpm = 1650;
  data[0] = ((rpm >> 8) & 255);
  data[1] = rpm & 255;
  Wire.write(data, 2);
}

void counter() {
  count++;
}