import discord
from discord.ext import commands
import wavelink
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Lavalink node settings
LAVALINK_HOST = "lava.link"
LAVALINK_PORT = 80
LAVALINK_PASSWORD = "youshallnotpass"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await wavelink.NodePool.create_node(
        bot=bot,
        host=LAVALINK_HOST,
        port=LAVALINK_PORT,
        password=LAVALINK_PASSWORD,
        region='us_central'
    )

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect(cls=wavelink.Player)
        await ctx.send(f"🎶 Joined {channel.name}!")
    else:
        await ctx.send("❌ You must be in a voice channel first.")

@bot.command()
async def play(ctx, *, search: str):
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        if ctx.author.voice:
            vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            return await ctx.send("❌ You're not in a voice channel!")

    if not vc.is_connected():
        await vc.connect(ctx.author.voice.channel)

    track = await wavelink.YouTubeTrack.search(search, return_first=True)
    await vc.play(track)
    await ctx.send(f"🎵 Now playing: **{track.title}**")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.voice_client.pause()
        await ctx.send("⏸️ Paused the song.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        await ctx.voice_client.resume()
        await ctx.send("▶️ Resumed the song.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped the song.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel.")

# ✅ Secure token from environment variable
bot.run(os.getenv("DISCORD_TOKEN"))
