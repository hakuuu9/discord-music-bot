import discord
from discord.ext import commands
import youtube_dl
import asyncio
from keep_alive import keep_alive
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

queue = {}
now_playing = {}

ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch'
}
ffmpeg_opts = {'options': '-vn'}
ytdl = youtube_dl.YoutubeDL(ytdl_opts)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

async def play_song(ctx, song):
    vc = ctx.voice_client
    info = ytdl.extract_info(song, download=False)
    url = info['url']
    title = info['title']
    vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
    now_playing[ctx.guild.id] = title
    await ctx.send(f"🎶 Now playing: **{title}**")

async def play_next(ctx):
    if queue[ctx.guild.id]:
        next_song = queue[ctx.guild.id].pop(0)
        await play_song(ctx, next_song)
    else:
        now_playing[ctx.guild.id] = None
        await ctx.voice_client.disconnect()

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Joined voice channel.")
    else:
        await ctx.send("You're not in a voice channel.")

@bot.command()
async def play(ctx, *, song):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("Join a voice channel first.")

    if ctx.guild.id not in queue:
        queue[ctx.guild.id] = []

    vc = ctx.voice_client
    if not vc.is_playing():
        await play_song(ctx, song)
    else:
        queue[ctx.guild.id].append(song)
        await ctx.send("🎵 Added to queue.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭ Skipped current song.")
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸ Paused.")
    else:
        await ctx.send("Nothing to pause.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed.")
    else:
        await ctx.send("Nothing is paused.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        queue[ctx.guild.id] = []
        await ctx.voice_client.disconnect()
        await ctx.send("⏹ Stopped and left the channel.")
    else:
        await ctx.send("Not connected to any voice channel.")

@bot.command()
async def queue_list(ctx):
    if ctx.guild.id in queue and queue[ctx.guild.id]:
        q = '\n'.join([f"{i+1}. {song}" for i, song in enumerate(queue[ctx.guild.id])])
        await ctx.send(f"📃 Queue:\n{q}")
    else:
        await ctx.send("Queue is empty.")

@bot.command()
async def np(ctx):
    now = now_playing.get(ctx.guild.id)
    if now:
        await ctx.send(f"🎧 Now playing: **{now}**")
    else:
        await ctx.send("Nothing is playing right now.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected.")
    else:
        await ctx.send("I'm not in a voice channel.")

keep_alive()
bot.run(TOKEN)