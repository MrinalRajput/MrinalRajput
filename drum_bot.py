import discord
from discord.ext import commands
from datetime import datetime
import random

bot = commands.Bot(command_prefix = ">")
restricted_words = ["gooh","kutta","kutte","harami","skyra"]

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.yfzVgB8hHizDFH7hSMTORIv5weg"

@bot.event
async def on_ready():
    print("I m Ready!")

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"{ctx.author.mention}")

@bot.command()
async def time(ctx):
    currenttime = datetime.now()
    await ctx.send(f"Current Time is {currenttime}")
    
@bot.listen()
async def on_message(message):
    if ("smp" in message.content.lower() or "server" in message.content.lower()) and (" on" in message.content.lower() or "online" in message.content.lower() or "offline" in message.content.lower() or "off" in message.content.lower()):
        await message.channel.send(f"{message.author.mention} Please Check <#877777208108789770> for Live Updates of Smp")
        
@bot.command()
async def tell(ctx, *, msg):
    await ctx.send(f"{msg}")

@bot.command()
async def info(ctx):
    Listedgreetings = ["Hello!","Hi!","Hey!","Heya!"]
    RandomGreetings = random.choice(Listedgreetings)
    await ctx.send(f"> {RandomGreetings} I am Tornax a Multi-Talented Discord Bot, Designed, Created and Configured by MrinalSparks")

@bot.command()
async def about(ctx):
    await ctx.send(f"> Tornax is a Multi-Talented and Friendly Bot, Use Tornax for moderation, server managements, streams and giveaways now!")

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    for word in restricted_words:
        if message.content.count(word)>0:
            await message.channel.purge(limit = 1)
    await bot.process_commands(message)

bot.run(TOKEN)