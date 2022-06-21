import json
import discord
import time
from steam_sales import *


with open("../bot_info.json", "r") as webhook_file:
    bot_info  = json.load(webhook_file)
    intents = discord.Intents.default()
    client = discord.Client()
    TOKEN = bot_info["TOKEN"]



@client.event
async def on_message(message):

    msg = message.content

    if msg.lower() == "!steamsales":
        response = cdn_top_sellers()
        send_cdn_info(response)
        time.sleep(5)

    if msg.lower() == "!steamsales"
client.run(TOKEN)