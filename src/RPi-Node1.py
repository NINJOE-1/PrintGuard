'''
This file contains all the code for the main raspberry pi of the system.
This contains the main periodic loop that gathers sensor info and
adds it to the firebase and notifies the user if something is off.
Written by Joseph Vretenar
'''

# declare import libraries
import smbus
import sys
import pyrebase
import socket
import discord
from discord.ext import commands
import asyncio
from time import sleep
import info
import PrusaLinkWrapper
from datetime import datetime

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

# setup discord config
intents = discord.Intents.default()
intents.presences = False
bot_token = info.botToken
bot = commands.Bot(command_prefix='!', intents=intents)

# setup i2c busses
bus = smbus.SMBus(1)
fanAddress = 0x08
sensorAddress = 0x09
cameraAddress = 0x0a

# tables on firebase
table1 = "SensorData"
table2 = "PrinterData"

# send discord message function
async def send_discord_message(bot, message) :
    try:
        await bot.wait_until_ready()
        channel = bot.get_channel(1213212262316376085)
        await channel.send(message)
    except Exception as e:
        print(f"Error sending Discord message: {e}")

# main function
def main() :
    while True:
        bus.write_byte(sensorAddress, 0x01)		# request data from sensor arduino
        dhtData = bus.read_i2c_block_data(sensorAddress, 0x00, 4)	# read data from sensor arduino
        bus.write_byte(fanAddress, dhtData[0])	# write the internal temp to the fan arduino
        sleep(1)								# wait for rpm to be calculated
        rpmData = bus.read_i2c_block_data(fanAddress, 0x00, 2)		# read rpm from fan arduino
        rpm = ((rpmData[0] << 8) | rpmData[1])	# calculate true rpm from data
        sensorData = [dhtData[0], dhtData[1], dhtData[2], dhtData[3], rpm]
        
        nozzle = printer.getNozzle()			# get nozzle temp
        bed = printer.getBed()					# get bed temp
        printerData = [nozzle, bed]
        
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')			# measure current time
        
        # record all data on firebase
        db.child(table1).child("internalTemp").child(time).set(sensorData[0])
        db.child(table1).child("internalHumidity").child(time).set(sensorData[1])
        db.child(table1).child("externalTemp").child(time).set(sensorData[2])
        db.child(table1).child("externalHumidity").child(time).set(sensorData[3])
        db.child(table1).child("fanSpeed").child(time).set(sensorData[4])
        db.child(table2).child("nozzleTemp").child(time).set(printerData[0])
        db.child(table2).child("bedTemp").child(time).set(printerData[1])
        
        # if the printer is printing, get progress
        if (printer.getPrintingStatus()):
            progress = printer.getProgress()
            db.child(table3).child("progress").child(time).set(progress)
        
        # check if temperature should provide a warning
        if (sensorData[0] > 35):
            message = ("Potential error: internal temp is " + str(sensorData[0]))
            #send_discord_message(bot, message)
        
        sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)