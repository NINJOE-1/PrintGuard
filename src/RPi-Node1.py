import smbus
import sys
import pyrebase
import socket
import discord
from discord.ext import commands
from time import sleep
import info
import PrusaLinkWrapper
from datetime import datetime

config = {
    "apiKey": info.firebaseAPI,
    "authDomain": info.firebaseAuth,
    "databaseURL": info.firebaseURL,
    "storageBucket": info.firebaseStorage
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

printer = PrusaLinkWrapper.PrusaLinkWrapper(info.printerIP, info.printerKey)

intents = discord.Intents.default()
intents.presences = False
bot_token = info.botToken
bot = commands.Bot(command_prefix='!', intents=intents)

bus = smbus.SMBus(1)
fanAddress = 0x08
sensorAddress = 0x09
cameraAddress = 0x0a

table1 = "SensorData"
table2 = "PrinterData"

sensorTable = ["internalTemp", "internalHumidity", "externalTemp", "externalHumidity", "fanSpeed"]
printerTable = ["nozzleTemp", "bedTemp", "progress"]

async def send_discord_message(bot, message):
        try:
            channel = bot.get_channel(info.channelId)
            await channel.send(message)
        except Exception as e:
            print(f"Error sending Discord message: {e}")

def main():
    key = 1
    while True:
        bus.write_byte(sensorAddress, 0x01)
        dhtData = bus.read_i2c_block_data(sensorAddress, 0x00, 4)
        bus.write_byte(fanAddress, dhtData[0])
        sleep(1)#wait for rpm to be calculated
        rpmData = bus.read_i2c_block_data(fanAddress, 0x00, 2)
        rpm = ((rpmData[0] << 8) | rpmData[1])
        sensorData = [dhtData[0], dhtData[1], dhtData[2], dhtData[3], rpm]
        
        nozzle = printer.getPrinter().json()["telemetry"]["temp-nozzle"]
        bed = printer.getPrinter().json()["telemetry"]["temp-bed"]
        #progress = printer.getStatus().json()["job"]["progress"]
        printerData = [nozzle, bed]
        
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.child(table1).child("internalTemp").child(time).set(sensorData[0])
        db.child(table1).child("internalHumidity").child(time).set(sensorData[1])
        db.child(table1).child("externalTemp").child(time).set(sensorData[2])
        db.child(table1).child("externalHumidity").child(time).set(sensorData[3])
        db.child(table1).child("fanSpeed").child(time).set(sensorData[4])
        
        db.child(table2).child("nozzleTemp").child(time).set(printerData[0])
        db.child(table2).child("bedTemp").child(time).set(printerData[1])
        #db.child(table3).child("progress").child(time).set(printerData[2])
        
        sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
        sys.exit(0)