import hikari
import lightbulb
import lavaplayer
from dotenv import load_dotenv
import os
import asyncio
import json
import random
import logging
from datetime import datetime, timedelta

plugin = lightbulb.Plugin("Music", "Music Extension")
load_dotenv()

lavalink = lavaplayer.LavalinkClient(
    host=os.getenv("HOST"),
    password=os.getenv("PASSWORD"),
    port=os.getenv("PORT"),
    is_ssl=True)


@plugin.listener(hikari.StartedEvent)
async def on_start(event: hikari.StartedEvent):
    lavalink.set_user_id(plugin.bot.get_me().id)
    lavalink.set_event_loop(asyncio.get_event_loop())
    lavalink.connect()


@plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent):
    await lavalink.raw_voice_state_update(event.guild_id, event.state.user_id, event.state.session_id,
                                          event.state.channel_id)


@plugin.listener(hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: hikari.VoiceServerUpdateEvent):
    await lavalink.raw_voice_server_update(event.guild_id, event.endpoint, event.token)


@plugin.listener(hikari.StartedEvent)
async def on_start(event: hikari.StartedEvent):
    with open('settings.json', 'r') as f:
        data = json.load(f)
    songs = data["playlist"]
    guild = data["guild"]
    channel = data["channel"]
    f.close()

    await asyncio.sleep(2)

    await plugin.bot.update_voice_state(guild, channel, self_deaf=True)
    await lavalink.wait_for_connection(guild)
    logging.info("Joined voice channel")
    await asyncio.sleep(2)
    result = await lavalink.auto_search_tracks(songs)
    await lavalink.add_to_queue(guild, result.tracks)
    await lavalink.shuffle(guild)
    await lavalink.repeat(guild, True)


@plugin.command()
@lightbulb.command(name="np", description="Shows you the current playing mix")
@lightbulb.implements(lightbulb.SlashCommand)
async def np_command(ctx: lightbulb.context.Context):
    node = await lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.queue:
        await ctx.respond("Nothing playing!")
        return
    await ctx.respond(f"[{node.queue[0].title}]({node.queue[0].uri})")
    # print(timedelta(milliseconds=round(node.queue[0].position)))
    # print(timedelta(milliseconds=round(node.queue[0].length)))


@plugin.command()
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("skip", "Skips the current mix (Admin only)")
@lightbulb.implements(lightbulb.SlashCommand)
async def skip_command(ctx: lightbulb.Context):
    await lavalink.skip(ctx.guild_id)
    await ctx.respond("Skipped the current song!")


@lavalink.listen(lavaplayer.TrackStartEvent)
async def track_start_event(event: lavaplayer.TrackStartEvent):
    logging.info(f"start track: {event.track.title}")
    await plugin.bot.update_presence(
        status=hikari.Status.IDLE,
        activity=hikari.Activity(
            name=event.track.title,
            type=hikari.ActivityType.LISTENING,
        ),
    )


@lavalink.listen(lavaplayer.TrackEndEvent)
async def track_end_event(event: lavaplayer.TrackEndEvent):
    logging.info(f"track end: {event.track.title}")


@lavalink.listen(lavaplayer.WebSocketClosedEvent)
async def web_socket_closed_event(event: lavaplayer.WebSocketClosedEvent):
    logging.error(f"error with websocket {event.reason}")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
