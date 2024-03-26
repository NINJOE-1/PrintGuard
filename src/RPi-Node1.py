import smbus
import sys
#import pyrebase
from time import sleep
import info
import PrusaLinkWrapper
'''
config = {
    "apiKey": info.firebaseAPI,
    "authDomain": info.firebaseAuth,
    "databaseURL": info.firebaseURL,
    "storageBucket": info.firebaseStorage
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

printer = PrusaLinkWrapper.PrusaLinkWrapper(info.printerIP, info.printerKey)
'''
bus = smbus.SMBus(1)
fanAddress = 0x08
sensorAddress = 0x09
cameraAddress = 0x0a

def main():
    while True:
        sleep(1)
        bus.write_byte(sensorAddress, 0x01)
        dhtData = bus.read_i2c_block_data(sensorAddress, 0x00, 4)
        iTemp = dhtData[0]
        iHum = dhtData[1]
        oTemp = dhtData[2]
        oHum = dhtData[3]
        print("Inner Temp: " + str(iTemp))
        print("Inner Hum: " + str(iHum))
        print("Outer Temp: " + str(oTemp))
        print("Outer Hum: " + str(oHum))
        sleep(1)
        bus.write_byte(fanAddress, 0x01)
        sleep(1)
        rpmData = bus.read_i2c_block_data(fanAddress, 0x00, 2)
        print("High byte: " + str(rpmData[0]))
        print("Low byte: " + str(rpmData[1]))
        rpm = ((rpmData[0] << 8) | rpmData[1])
        print("Rpm speed is: " + str(rpm))
        sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
        sys.exit(0)