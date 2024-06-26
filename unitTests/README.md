# Unit Testing

## DHT11 Sensor Testing
The DHT11 sensors are the main temperature and humidity monitoring for the Print Guard system. To test that these sensors are operational the system will monitor both temperature sensors right next to each other and make sure the current temperature is the same betweent the two.

## Temperature Error Testing
To check for errors, the system will watch the data from the temperature sensor. To test this functionality we wrote an array list to test a range of values to verify that the temperature changing gets detected, and will alert the user if the value are below or above the optimal range.

## Fan Testing
The 120mm case fan will be used to control the temperature of the enclosure based on the temperature from the DHT11 sensors. To test that the fan is operational to it's full extent, the system will vary the speed from 0% to 100% and check the RPM on the sense pin to make sure it reads the expected value.

## Camera Testing
The camera will be used to monitor the printer throughout the print. It needs to be able to take photos and stream video. To test this functionality, the system will take photos and stream video.

## 3D Printer Testing
The printer is the main device in the print guard system. The printer will be able to be stopped by the user, and can also send sensor data to the main RPi. To test this, the system will check the temperature of the nozzle, and then stop the current print.

## Database Testing
The database holds all the data for the printer and the enclosure sensors. The system will send fake data to the database and pull it back to make sure it can properly update the data.

## Website Control Testing
The website is the main viewing and control system for the print guard system. To test the system, the user will press the verify system button which will verify that the user can control the system from the website.

## Notification Testing
The notifications will be used to alert the user of any errors with the print as well as notifying the user that the print has finished. This test will be directly linked with the database test which will send a notification to discord saying test passed when the database test finishes.
