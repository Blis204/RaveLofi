import hikari
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

bot = hikari.GatewayBot(token=os.getenv("TOKEN"))


@bot.listen()
async def on_start(event: hikari.StartedEvent):
    print("Bot has started")


bot.run()
