import discord
from discord.ext import commands,tasks
import os
import asyncio
from dotenv import load_dotenv
import yt_dlp as youtube_dl

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]

#

youtube_dl.utils.bug_reports_message = lambda *args, **kwargs: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(url, download=False)
        )

        if 'entries' in data:
            data = data['entries'][0]

        return data

#

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)

@bot.event
async def on_ready():
    print( "Please welcome the bot to the server, and kindly treat it with respect." )

@bot.event
async def on_message(message):
    if message.content.startswith("!!hello"):
        await message.channel.send("Hello.")
    else:
        await bot.process_commands(message)

@bot.command(name='join', help='Allow for the bot to join the designated voice channel.')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} never joined a voice channel to allow for the bot entry. Please join a channel first.".format(ctx.message.author.name))
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await ctx.send( "The bot already joined a voice channel within the server." )

@bot.command(name='leave', help='Allow for the bot to leave the recently joined channel.')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send( "The bot never joined a voice channel." )
    if not ctx.message.author.voice:
        await ctx.send( "The users must first join a voice channel to ask the bot to depart from one." )

@bot.command(name='hello', help='The bot shall respond with a kind gesture.')
async def hello(ctx):
    await ctx.send( "Hello." )

@bot.command(name='information', help='The bot shall respond with information regarding its feature-set.')
async def information(ctx):
    await ctx.send( "This bot runs on Python, focusing on the playback of music." )

@bot.command(name='play', help='Users may play a song through YouTube.')
async def play(ctx, url):

    voice_client = ctx.guild.voice_client

    if voice_client is None:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("Join a voice channel first.")
            return

    try:
        async with ctx.typing():
            #
            data = await bot.loop.run_in_executor(
                None,
                lambda: ytdl.extract_info(url, download=False)
            )

            audio_url = data['url']

            source = discord.FFmpegPCMAudio(
                audio_url,
                executable="ffmpeg",
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn"
            )

            voice_client.play(source)

            await ctx.send(f'**Now playing:** {data["title"]}')
            #
    except Exception as e:
        await ctx.send(f"Playback error: {e}")

@bot.command(name='pause', help='The bot shall pause the queue, awaiting an eventual play command.')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send( "The bot exists as currently empty in the queue." )

@bot.command(name='resume', help='The bot eventually resumes the music, after initially pausing it earlier.')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send( "The queue for the bot never experienced a pause in play." )

@bot.command(name='stop', help='Users may immediately stop any playback of the queue, emptying it.')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send( "The queue already existed as inactive prior to the command." )

if __name__ == "__main__":
    bot.run( TOKEN )