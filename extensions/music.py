import hikari
import lightbulb
import lavaplayer
from dotenv import load_dotenv
import os
import asyncio
import json
import random
import logging

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


# On voice state update the bot will update the lavalink node


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
    songs = data["songs"]
    guild = data["guild"]
    channel = data["channel"]
    f.close()
    song = random.choice(songs)
    await asyncio.sleep(2)
    await plugin.bot.update_voice_state(guild, channel, self_deaf=True)
    await lavalink.wait_for_connection(guild)
    print("[INFO] Joined voice channel")
    await asyncio.sleep(2)

    result = await lavalink.auto_search_tracks("https://www.youtube.com/watch?v=iBAEt06J2Ho")
    await lavalink.play(guild, result[0], 404574824795471872)


@lavalink.listen(lavaplayer.TrackStartEvent)
async def track_start_event(event: lavaplayer.TrackStartEvent):
    logging.info(f"start track: {event.track.title}")


@lavalink.listen(lavaplayer.TrackEndEvent)
async def track_end_event(event: lavaplayer.TrackEndEvent):
    logging.info(f"track end: {event.track.title}")
    with open('settings.json', 'r') as f:
        data = json.load(f)
    songs = data["songs"]
    guild = data["guild"]
    channel = data["channel"]
    f.close()
    song = random.choice(songs)
    result = await lavalink.auto_search_tracks(song)
    await lavalink.play(guild, result[0], 404574824795471872)


@lavalink.listen(lavaplayer.WebSocketClosedEvent)
async def web_socket_closed_event(event: lavaplayer.WebSocketClosedEvent):
    logging.error(f"error with websocket {event.reason}")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
