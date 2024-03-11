#Written by Samuel Mauricla

import pyrebase
from time import sleep
from info import firebaseAPI, firebaseAuth, firebaseURL, firebaseStorage

config = { # setup config for firebase
    "apiKey": firebaseAPI,
    "authDomain": firebaseAuth,
    "databaseURL": firebaseURL,
    "storageBucket": firebaseStorage
}

# initializations
firebase = pyrebase.initialize_app(config)
db = firebase.database()
internal = "internalTemp"
fan = "fanSpeed"
table = "SensorData"

# get the data of the user
data = db.child(table).child(internal).get()


key = 0

count = 0
db.child(table).child(fan).child(key).set(0) # input data
key += 1 # increment key
count += 1 # increment how many data points entered so far
sleep (1) # sleep for 1 second