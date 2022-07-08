import json
import discord
import time
from steam_sales import *


with open("../bot_info.json", "r") as webhook_file:
    bot_info  = json.load(webhook_file)
    intents = discord.Intents.default()
    client = discord.Client()
    DIG_CHANNEL = bot_info['DIG_CHANNEL']
    TOKEN = bot_info["TOKEN"]



@client.event
async def on_message(message):
    msg = message.content

    if msg.lower() == "!steamsales":
        response = top_sellers()
        send_info(response)
        time.sleep(5)

    if msg.lower() == "!steambot":
        response = "!steamsales to see top selling Steam games in Canada\n"
        await message.channel.send(response)
client.run(TOKEN)