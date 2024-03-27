#include <Wire.h>

#define ADDRESS 0x08
#define PWMPIN 9
#define RPMPIN 2

volatile uint8_t pwm = 0;
uint32_t count = 0;
uint8_t data [] = {0, 0};
unsigned long start_time;
uint16_t rpm;
uint8_t incoming;
uint8_t measure = 0;

void setup() {
  Wire.begin(ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  pinMode(PWMPIN, OUTPUT);
  pinMode(RPMPIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(RPMPIN), counter, RISING);
}

void loop() {
  if (measure == 1) {
    count = 0;
    start_time = millis();
    while((millis() - start_time) < 1000) {}
    rpm = (count * 30);
    measure = 0;
  }
}

void receiveData(int byteCount) {
  incoming = Wire.read();
  if (incoming == 0) {
  } else if (incoming < 31) {
    pwm = 0;
    analogWrite(PWMPIN, pwm);
  } else if (incoming >= 31 && incoming < 34) {
    pwm = 127;
    analogWrite(PWMPIN, pwm);
  } else {
    pwm = 255;
    analogWrite(PWMPIN, pwm);
  }
  measure = 1;
}

void sendData() {
  data[0] = ((rpm >> 8) & 255);
  data[1] = rpm & 255;
  Wire.write(data, 2);
}

void counter() {
  count++;
}
