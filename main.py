import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()


client = commands.Bot(command_prefix=">>", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Bot Online!")

client.run(os.getenv("TOKEN"))
