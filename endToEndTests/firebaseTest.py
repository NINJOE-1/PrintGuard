import pyrebase
from time import sleep

config = { # setup config for firebase
    "apiKey": "AIzaSyBUG_CMNlYEh0j63f4YwQJGle6rfx4ZU_I",
    "authDomain": "print-guard.firebaseapp.com",
    "databaseURL": "https://print-guard-default-rtdb.firebaseio.com/",
    "storageBucket": "print-guard.appspot.com"
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