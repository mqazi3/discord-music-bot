import asyncio
import os

import discord
import yt_dlp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]

yt_dlp.utils.bug_reports_message = lambda *args, **kwargs: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

FFMPEG_BEFORE_OPTIONS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
FFMPEG_OPTIONS = "-vn"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!!", intents=intents)


@bot.event
async def on_ready():
    print("Please welcome the bot to the server, and kindly treat it with respect.")


@bot.command(name="join", help="Allow for the bot to join the designated voice channel.")
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send(
            f"{ctx.author.name} never joined a voice channel to allow for the bot entry. "
            "Please join a channel first."
        )
        return

    voice_client = ctx.guild.voice_client
    if voice_client is not None and voice_client.is_connected():
        await ctx.send("The bot already joined a voice channel within the server.")
        return

    await ctx.author.voice.channel.connect()


@bot.command(name="leave", help="Allow for the bot to leave the recently joined channel.")
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not voice_client.is_connected():
        await ctx.send("The bot never joined a voice channel.")
        return

    await voice_client.disconnect()


@bot.command(name="hello", help="The bot shall respond with a kind gesture.")
async def hello(ctx):
    await ctx.send("Hello.")


@bot.command(name="information", help="The bot shall respond with information regarding its feature-set.")
async def information(ctx):
    await ctx.send("This bot runs on Python, focusing on the playback of music.")


@bot.command(name="play", help="Users may play a song through YouTube.")
async def play(ctx, url):
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
                lambda: ytdl.extract_info(url, download=False),
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

    except Exception as e:
        await ctx.send(f"Playback error: {e}")


@bot.command(name="pause", help="The bot shall pause the current audio, awaiting an eventual resume command.")
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not voice_client.is_playing():
        await ctx.send("Nothing is currently playing.")
        return

    voice_client.pause()


@bot.command(name="resume", help="The bot eventually resumes the music, after initially pausing it earlier.")
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not voice_client.is_paused():
        await ctx.send("The audio is not paused.")
        return

    voice_client.resume()


@bot.command(name="stop", help="Users may immediately stop any playback.")
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client is None or not (voice_client.is_playing() or voice_client.is_paused()):
        await ctx.send("Nothing is currently playing.")
        return

    voice_client.stop()


if __name__ == "__main__":
    bot.run(TOKEN)