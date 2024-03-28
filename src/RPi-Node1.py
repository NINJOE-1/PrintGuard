'''
This file contains all the code for the main raspberry pi of the system.
This contains the main periodic loop that gathers sensor info and
adds it to the firebase and notifies the user if something is off.
Written by Joseph Vretenar
'''

# declare import libraries
import os
import smbus
import sys
import pyrebase
import requests
from time import sleep
import info
import PrusaLinkWrapper
from datetime import datetime
import base64
#from PIL import image

# setup firebase config
config = {
    "apiKey": info.firebaseAPI,
    "authDomain": info.firebaseAuth,
    "databaseURL": info.firebaseURL,
    "storageBucket": info.firebaseStorage
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# setup printer config
printer = PrusaLinkWrapper.PrusaLinkWrapper(info.printerIP, info.printerKey)

# setup i2c busses
bus = smbus.SMBus(1)
fanAddress = 0x08
sensorAddress = 0x09
cameraAddress = 0x0a

# tables on firebase
t1 = "SensorData"
t2 = "PrinterData"
t3 = "Errors"


def convertImageToByte(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    return image_base64


# main function
def main():
    while True:
        # request data from arduino sensors
        bus.write_byte(sensorAddress, 0x01)
        # read data from arduino sensors
        dhtData = bus.read_i2c_block_data(sensorAddress, 0x00, 4)
        # write the internal temp to the fan arduino
        bus.write_byte(fanAddress, dhtData[0])
        # wait for the rpm to be calculated
        sleep(1)
        # read the rpm from the fan arduino
        rpmData = bus.read_i2c_block_data(fanAddress, 0x00, 2)
        # calculate true rpm from two bytes
        rpm = ((rpmData[0] << 8) | rpmData[1])
        # combine all sensor data
        sensorData = [dhtData[0], dhtData[1], dhtData[2], dhtData[3], rpm]
        # get printer sensors
        nozzle = printer.getNozzle()    # get nozzle temp
        bed = printer.getBed()          # get bed temp
        printerData = [nozzle, bed]
        # measure current time
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # record all data on firebase
        db.child(t1).child("internalTemp").child(time).set(sensorData[0])
        db.child(t1).child("internalHumidity").child(time).set(sensorData[1])
        db.child(t1).child("externalTemp").child(time).set(sensorData[2])
        db.child(t1).child("externalHumidity").child(time).set(sensorData[3])
        db.child(t1).child("fanSpeed").child(time).set(sensorData[4])
        db.child(t2).child("nozzleTemp").child(time).set(printerData[0])
        db.child(t2).child("bedTemp").child(time).set(printerData[1])
        os.system("libcamera-still -o images/capture.jpg")
        db.child(t2).child("image").child(time).set({"image_data": convertImageToByte("images/capture.jpg")})
        # if the printer is printing, get progress
        if (printer.getPrintingStatus()):
            progress = printer.getProgress()
            db.child(t2).child("progress").child(time).set(progress)
        # check for errors and notify user
        if (sensorData[0] > 35):
            error = 'Internal temperature is at  ' + str(sensorData[0]) + '°C'
            payload = {'content': (error)}
            requests.post(info.DISCORD_WEBHOOK_URL, json=payload)
            db.child(t3).child("error").child(time).set(error)
            if (sensorData[4] == 0):
                error = 'Fan is not running'
                payload = {'content': (error)}
                requests.post(info.DISCORD_WEBHOOK_URL, json=payload)
                db.child(t3).child("error").child(time).set(error)
        elif (sensorData[0] > 31 and sensorData[4] == 0):
            error = 'Fan is not running'
            payload = {'content': (error)}
            requests.post(info.DISCORD_WEBHOOK_URL, json=payload)
            db.child(t3).child("error").child(time).set(error)
        elif (sensorData[0] < 31 and sensorData[4] > 100):
            error = 'Fan is stuck running'
            payload = {'content': (error)}
            requests.post(info.DISCORD_WEBHOOK_URL, json=payload)
            db.child(t3).child("error").child(time).set(error)
        sleep(30)


if __name__ == '__main__':
    try:
        payload = {'content': 'Print Guard is now operational'}
        response = requests.post(info.DISCORD_WEBHOOK_URL, json=payload)
        main()
    except KeyboardInterrupt:
        sys.exit(0)
