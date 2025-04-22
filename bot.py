import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎶 Joined {channel.name}!")
    else:
        await ctx.send("❌ You must be in a voice channel.")

@bot.command()
async def play(ctx, *, query):
    if not ctx.author.voice:
        return await ctx.send("❌ Join a voice channel first.")

    voice = ctx.voice_client
    if not voice:
        voice = await ctx.author.voice.channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'auto',  # supports SoundCloud & YouTube
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]  # first result
        url = info["url"]
        title = info.get("title", "Unknown track")

    source = await discord.FFmpegOpusAudio.from_probe(url, method='fallback')
    voice.play(source)
    await ctx.send(f"🎵 Now playing: **{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel.")

# Token from Render environment
bot.run(os.getenv("DISCORD_TOKEN"))
