import os
import discord
from discord.ext import commands
import wavelink

# Ensure custom ffmpeg binary works on Render
os.environ["PATH"] = os.getcwd() + "/ffmpeg:" + os.environ["PATH"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    # Connect to Lavalink node
    await wavelink.NodePool.connect(
        client=bot,
        host='lava.link',  # Use your own Lavalink if you set one up
        port=80,
        password='youshallnotpass',
        https=False
    )

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        return await ctx.send("❌ You are not in a voice channel.")
    
    vc = ctx.author.voice.channel
    player: wavelink.Player = await vc.connect(cls=wavelink.Player)
    await ctx.send(f"🔊 Joined {vc.name}")

@bot.command()
async def play(ctx, *, search: str):
    player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)

    if not player.is_connected():
        if ctx.author.voice:
            await ctx.invoke(bot.get_command("join"))
        else:
            return await ctx.send("❌ You're not in a voice channel.")

    track = await wavelink.YouTubeTrack.search(search, return_first=True)
    await player.play(track)
    await ctx.send(f"🎶 Now playing: **{track.title}**")

@bot.command()
async def pause(ctx):
    player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
    await player.pause()
    await ctx.send("⏸ Paused.")

@bot.command()
async def resume(ctx):
    player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
    await player.resume()
    await ctx.send("▶️ Resumed.")

@bot.command()
async def stop(ctx):
    player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
    await player.stop()
    await ctx.send("⏹ Stopped playback.")

@bot.command()
async def leave(ctx):
    player: wavelink.Player = wavelink.NodePool.get_node().get_player(ctx.guild)
    await player.disconnect()
    await ctx.send("👋 Left the voice channel.")

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
