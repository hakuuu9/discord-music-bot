import discord
from discord.ext import commands
import yt_dlp
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, url):
    if not ctx.author.voice:
        return await ctx.send("You need to be in a voice channel first.")

    voice_channel = ctx.author.voice.channel

    # Connect to voice channel if not already
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        vc = ctx.voice_client
        await vc.move_to(voice_channel)

    # Extract audio URL
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info['url']
        title = info.get('title', 'Unknown title')

    # Play the audio using FFmpeg from remote source
    ffmpeg_options = {
        'options': '-vn'
    }

    source = await discord.FFmpegOpusAudio.from_probe(stream_url, **ffmpeg_options)
    vc.play(source)

    await ctx.send(f"Now playing: **{title}**")

@bot.command(name='stop', help='Stops the music and disconnects')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Stopped and disconnected.")
    else:
        await ctx.send("I'm not in a voice channel.")

bot.run("YOUR_BOT_TOKEN")
