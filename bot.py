import asyncio
import logging
import os

import discord
import yt_dlp
from discord.ext import commands
from dotenv import load_dotenv

log = logging.getLogger("musicbot")

yt_dlp.utils.bug_reports_message = lambda *args, **kwargs: ""

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to IPv4; some hosts have IPv6 routing issues
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

# Reconnect if the audio stream drops mid-song instead of ending playback
FFMPEG_BEFORE_OPTIONS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
FFMPEG_OPTIONS = "-vn"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!!", intents=intents)


@bot.event
async def on_ready():
    log.info("Logged in as %s in %d server(s)", bot.user, len(bot.guilds))


@bot.command(name="join", help="Join your current voice channel.")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first.")
        return

    voice_client = ctx.guild.voice_client
    if voice_client is not None and voice_client.is_connected():
        await ctx.send("I'm already in a voice channel on this server.")
        return

    await ctx.author.voice.channel.connect()


@bot.command(name="leave", help="Leave the voice channel.")
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not voice_client.is_connected():
        await ctx.send("I'm not in a voice channel.")
        return

    await voice_client.disconnect()


@bot.command(name="hello", help="Say hello.")
async def hello(ctx):
    await ctx.send("Hello.")


@bot.command(name="information", help="Show what this bot does.")
async def information(ctx):
    await ctx.send("A Python music bot: use !!play <url or search terms> in a voice channel.")


@bot.command(name="play", help="Play audio from a URL or search terms.")
async def play(ctx, *, query: str):
    voice_client = ctx.guild.voice_client

    if voice_client is None:
        if ctx.author.voice is None:
            await ctx.send("Join a voice channel first.")
            return
        voice_client = await ctx.author.voice.channel.connect()

    try:
        async with ctx.typing():
            # yt-dlp is blocking, so run it in a thread to keep the bot responsive
            loop = asyncio.get_running_loop()
            data = await loop.run_in_executor(
                None,
                lambda: ytdl.extract_info(query, download=False),
            )

            # Searches and playlists return a list of results; take the first one
            if "entries" in data:
                data = data["entries"][0]

            source = discord.FFmpegPCMAudio(
                data["url"],
                executable="ffmpeg",
                before_options=FFMPEG_BEFORE_OPTIONS,
                options=FFMPEG_OPTIONS,
            )

            # Replace whatever is playing instead of raising "Already playing audio"
            if voice_client.is_playing() or voice_client.is_paused():
                voice_client.stop()

            voice_client.play(source)

        await ctx.send(f"**Now playing:** {data['title']}")

    except Exception:
        # Full details go to the logs; users get a short message without internals
        log.exception("Playback failed for query %r in guild %s", query, ctx.guild.id)
        await ctx.send("Couldn't play that. Check the link or try different search terms.")


@bot.command(name="pause", help="Pause the current audio.")
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not voice_client.is_playing():
        await ctx.send("Nothing is playing.")
        return

    voice_client.pause()


@bot.command(name="resume", help="Resume paused audio.")
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not voice_client.is_paused():
        await ctx.send("The audio isn't paused.")
        return

    voice_client.resume()


@bot.command(name="stop", help="Stop the current audio.")
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not (voice_client.is_playing() or voice_client.is_paused()):
        await ctx.send("Nothing is playing.")
        return

    voice_client.stop()


def main():
    load_dotenv()
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN is not set. Copy .env.example to .env and add your bot token.")
    # discord.py sets up console logging for its own logger and the root logger
    bot.run(token, root_logger=True)


if __name__ == "__main__":
    main()
