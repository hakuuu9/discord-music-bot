import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Create bot instance
bot = commands.Bot(command_prefix="$")

# Event for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Command to join a voice channel and play music
@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, url):
    # Connect to voice channel
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'quiet': True,
        'logtostderr': False,
    }

    # Download the audio using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2))

    await ctx.send(f'Now playing: {info["title"]}')

# Command to stop the music
@bot.command(name='stop', help='Stops the music and disconnects from the voice channel')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    await ctx.send('Music stopped and disconnected.')

# Run the bot with the token
bot.run('YOUR_BOT_TOKEN')
