import smbus
import sys
import pyrebase
from time import sleep
from info import firebaseAPI, firebaseAuth, firebaseURL, firebaseStorage

config = { # setup config for firebase
    "apiKey": firebaseAPI,
    "authDomain": firebaseAuth,
    "databaseURL": firebaseURL,
    "storageBucket": firebaseStorage
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
internal = "internalTemp"
fan = "fanSpeed"
table = "SensorData"

data = db.child(table).child(internal).get()

key = 0

if data.val() != None:
    dataList = data.each()
    lastPoint = dataList[-1]
    key = lastPoint.key() + 1
else:
    key = 0


bus = smbus.SMBus(1)
fanAddress = 0x08
sensorAddress = 0x09
cameraAddress = 0x0a

def main():
    sensorGet = 0x01
    key = 0
    while 1:
        print("Requesting Sensor Data")
        bus.write_byte(sensorAddress,sensorGet)
        sensorData = bus.read_byte(sensorAddress)
        print("Sensor Data: " + str(sensorData))
        sleep(1)
        print("Sending Temp")
        bus.write_byte(fanAddress, sensorData)
        rpmSpeed = bus.read_byte(fanAddress)
        print("Fan Speed: " + str(rpmSpeed))
        db.child(table).child(internal).child(key).set(sensorData)
        db.child(table).child(fan).child(key).set(rpmSpeed)
        key += 1
        sleep(3)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
        sys.exit(0)
