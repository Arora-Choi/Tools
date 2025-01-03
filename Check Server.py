import discord
from discord.ext import commands
import requests

TOKEN = input("봇의 토큰 : ")
WEBHOOK_URL = input("웹훅 URL : ")

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def create_invite(guild):
    invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
    return invite

def send_webhook_message(guild_info):
    if WEBHOOK_URL:
        embed_data = {
            "embeds": [
                {
                    "title": "Discord Bot's Server",
                    "color": 0x97b6ed,
                    "fields": [
                        {
                            "name": "Servers",
                            "value": guild_info,
                        }
                    ],
                    "footer": {
                        "text": "Created By Arora | .gg/2Dp6sGfjas"
                    }
                }
            ],
            "username": "Arora",
            "avatar_url": "https://i.ibb.co/WxMXR2c/image.webp"
        }
        requests.post(WEBHOOK_URL, json=embed_data)

@bot.event
async def on_ready():
    guild_info = ""
    for guild in bot.guilds:
        invite = await create_invite(guild)
        guild_info += f'Server Name: {guild.name}\nServer ID: {guild.id}\nInvite: {invite}\n\n'
    
    if guild_info:
        await send_webhook_message(guild_info)
    else:
        print('서버를 찾을 수 없음.')

bot.run(TOKEN)