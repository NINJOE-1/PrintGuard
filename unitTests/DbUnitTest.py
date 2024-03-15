import pyrebase
from time import sleep
from info import firebaseAPI, firebaseAuth, firebaseURL, firebaseStorage
import socket
import requests
import discord
from discord.ext import commands
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
temp = 10
rpmSpeed = 2000
key = 0
db.child(table).child(internal).child(key).set(temp)
db.child(table).child(fan).child(key).set(rpmSpeed)

# get the data of the user
data = db.child(table).child(internal).get()
returnTemp = data.val()
data = db.child(table).child(fan).get()
returnFan = data.val()
print("returnTemp: " + str(returnTemp) + " returnRPM: " + str(returnFan))

# Define the intents
intents = discord.Intents.default()
intents.presences = False
# Discord bot setup with intents
bot_token = 'MTIwMDA4MjQ2MDI2NDkwNjgzNA.GtuMAw.lY6M8-DzJopP03d3OXMO7Z_fFlFCvMepr3kb_o'  # Replace with your Discord bot token
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_discord_message(bot, message):
        try:
            channel_id = 1213212262316376085 # Replace with your Discord channel ID
            channel = bot.get_channel(channel_id)
            await channel.send(message)
        except Exception as e:
            print(f"Error sending Discord message: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    if temp == returnTemp[0] and rpmSpeed == returnFan[0]:
        print("Test passed")
        message ="Test Passed"
        await send_discord_message(bot, message)
    else:
        print("Test Failed")
        message ="Test Failed"
        await send_discord_message(bot, message)
        
bot.run(bot_token)