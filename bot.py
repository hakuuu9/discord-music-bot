import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command(name='play', help='Plays a song from YouTube (link or search)')
async def play(ctx, *, query):
    if not ctx.author.voice:
        return await ctx.send("You need to be in a voice channel first.")

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        vc = ctx.voice_client
        await vc.move_to(voice_channel)

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        url = info['url']
        title = info.get('title', 'Unknown title')

    ffmpeg_opts = {'options': '-vn'}
    source = await discord.FFmpegOpusAudio.from_probe(url, **ffmpeg_opts)
    vc.play(source)

    await ctx.send(f"Now playing: **{title}**")

@bot.command(name='stop', help='Stops the music and disconnects')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Stopped and disconnected.")
    else:
        await ctx.send("I'm not in a voice channel.")

bot.run(os.environ["DISCORD_TOKEN"])
