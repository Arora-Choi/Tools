from os import system
mytitle = "Server Cloner"
system("title "+mytitle)
import discord
import asyncio
from colorama import Fore, init, Style
import platform
from serverclone import Clone

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
os = platform.system()
if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")
print(f"""{Fore.RED}
{Style.RESET_ALL}
        """)
token = input(f'토큰을 입력하시오 : \n >')
guild_s = input('복사할 서버 아이디 :\n >')
guild = input('붙여넣을 서버 아이디 :\n >')
input_guild_id = guild_s  # <-- input guild id
output_guild_id = guild  # <-- output guild id
token = token  # <-- your Account token


print("  ")
print("  ")

@client.event
async def on_ready():
    extrem_map = {}
    print(f"Logged in as {client.user}")
    print("Cloning Server")
    guild_from = client.get_guild(int(input_guild_id))
    guild_to = client.get_guild(int(output_guild_id))
    await Clone.channels_create(guild_to, guild_from)
    print(f"""{Fore.GREEN}
Cloned
    {Style.RESET_ALL}""")
    await asyncio.sleep(5)
    await client.close()


client.run(token)