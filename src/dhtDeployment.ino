#include <Wire.h>
#include <DHT.h>

#define ADDRESS 0x09
#define INNER 8
#define OUTER 7
#define DHTTYPE DHT11

DHT inner(INNER, DHTTYPE);
DHT outer(OUTER, DHTTYPE);

uint8_t iTemp, iHum, oTemp, oHum;
uint8_t data [] = {1, 1, 1, 1};

void setup() {
  Wire.begin(ADDRESS);
  Wire.onRequest(sendData);
  inner.begin();
  outer.begin();
}

void loop() {
  iTemp = inner.readTemperature();
  iHum = inner.readHumidity();
  oTemp = outer.readTemperature();
  oHum = outer.readHumidity();
  data[0] = iTemp;
  data[1] = iHum;
  data[2] = oTemp;
  data[3] = oHum;
}

// Handle request to send I2C data
void sendData() {
  Wire.write(data, 4);
}