import smbus
import sys
import pyrebase
from time import sleep
import info
import PrusaLinkWrapper

config = {
    "apiKey": info.firebaseAPI,
    "authDomain": info.firebaseAuth,
    "databaseURL": info.firebaseURL,
    "storageBucket": info.firebaseStorage
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

printer = PrusaLinkWrapper.PrusaLinkWrapper(info.printerIP, info.printerKey)

bus = smbus.SMBus(1)
fanAddress = 0x08
sensorAddress = 0x09
cameraAddress = 0x0a

def main():
    while(True) {
        #do stuff
        sleep(15000)
    }
