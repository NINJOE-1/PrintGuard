/* 
   Temperature and humidity sensor with two DHT22 sensors
   By: Basma Aboushaer - 101186291
*/

//Libraries
#include <DHT.h>;

//Constants
#define DHTPIN1 8    // Digital pin connected to the first DHT sensor
#define DHTPIN2 7    // Digital pin connected to the second DHT sensor
#define DHTTYPE DHT11   // DHT 11 (AM2302)

// Initialize DHT sensors
DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

//Variables
float hum1, temp1;  // Variables to store humidity and temperature from the first sensor
float hum2, temp2;  // Variables to store humidity and temperature from the second sensor

void setup() {
  Serial.begin(9600);
  dht1.begin();
  dht2.begin();
}

void loop() {
  delay(2000);

  // Read data from the first sensor and store it in variables hum1 and temp1
  hum1 = dht1.readHumidity();
  temp1 = dht1.readTemperature();

  // Read data from the second sensor and store it in variables hum2 and temp2
  hum2 = dht2.readHumidity();
  temp2 = dht2.readTemperature();

  // Print temperature and humidity values from the first sensor to the serial monitor
  Serial.print("Sensor 1 - Humidity: ");
  Serial.print(hum1);
  Serial.print(" %, Temp: ");
  Serial.print(temp1);
  Serial.println(" Celsius");

  // Print temperature and humidity values from the second sensor to the serial monitor
  Serial.print("Sensor 2 - Humidity: ");
  Serial.print(hum2);
  Serial.print(" %, Temp: ");
  Serial.print(temp2);
  Serial.println(" Celsius");

  if (temp1 > (temp2 + 2) || temp1 < (temp2 - 2))
    Serial.println("Test Failed: Temp1 out of range of Temp2");
  Serial.println("Test Passed: Temp1 in range of Temp2");


  delay(10000); // Delay before the next reading
}


