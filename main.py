import lightbulb
import hikari
from dotenv import load_dotenv
import os

load_dotenv()

bot = lightbulb.BotApp(token=os.getenv("TOKEN"), prefix=">>")


@bot.listen(hikari.StartedEvent)
async def on_start(event):
    print("Bot has started")


@bot.command
@lightbulb.command("ping", "checks if the bot is alive")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")

bot.run()
