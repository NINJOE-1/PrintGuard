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
    while True:
        bus.write_byte(sensorAddress, 0x01)
        dhtData = bus.read_i2c_block_data(sensorAddress, 0x00, 4)
        bus.write_byte(fanAddress, 0x01)
        sleep(1)	#wait for rpm to be calculated
        rpmData = bus.read_i2c_block_data(fanAddress, 0x00, 2)
        rpm = ((rpmData[0] << 8) | rpmData[1])
        sensorData = [dhtData[0], dhtData[1], dhtData[2], dhtData[3], rpm]
        
        nozzle = printer.getNozzle()
        bed = printer.getBed()
        progress = printer.getProgress()
        printerData = [nozzle, bed, progress]
        
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in sensorTable:
            db.child(table1).child(sensorTable[i]).child(time).set(sensorData[i])
        for j in printerTable:
            db.child(table2).child(printerTable[j]).child(time).set(printerData[j])
        sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
        sys.exit(0)