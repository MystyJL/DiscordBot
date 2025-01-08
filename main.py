import feedparser
import os
import discord
from dotenv import load_dotenv
from time import sleep

f = open("channels.txt","r")
channels = f.read().strip().split("\n")

def update():
    f = open("channels.txt","r")
    channels = f.read().strip().split("\n")
    return channels

load_dotenv()
message = "**{}**\n{}"
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL_ID')
client = discord.Client(intents=discord.Intents.default())

async def getFeed():
    feed_url = "https://orangemushroom.net/feed/"
    while True:
        f = open("memories.txt", "r")
        feed = feedparser.parse(feed_url)
        title = feed["entries"][0]["title"]
        link = feed["entries"][0]["links"][0]["href"]
        if f.read()==link:
            sleep(3600)
            continue
        else:
            writeFile = open("memories.txt", "w")
            writeFile.write(link)
            writeFile.close()
            await write_to_server(message.format(title,link))
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await getFeed()

        
async def write_to_server(payload):
    for channel in channels:
        c = client.get_channel(int(channel.strip()))
        await c.send(payload)
    

client.run(TOKEN)


    
    