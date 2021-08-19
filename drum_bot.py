import discord
from discord.ext import commands
from datetime import datetime
import random

client = commands.Bot(command_prefix = ">")
restricted_words = ["gooh","kutta","kutte","harami","skyra"]

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.yfzVgB8hHizDFH7hSMTORIv5weg"

@client.event
async def on_ready():
    print("I m Ready!")

@client.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

@client.command()
async def ping(ctx):
    await ctx.send(f"{ctx.author.mention}")

@client.command()
async def whoistattiman(ctx):
    await ctx.send(f"WickedSalasa is a Tatti Man")

@client.command()
async def time(ctx):
    currenttime = datetime.now()
    await ctx.send(f"Current Time is {currenttime}")
    
@client.event
async def on_message(message):
    if "?" in message.content:
        print("Working")
        await message.channel.send(f"{ctx.author.mention} Please Check #smp-chat for Live Updates of Smp")
        

@client.command()
async def tell(ctx, *, msg):
    await ctx.send(f"{msg}")

@client.command()
async def info(ctx):
    Listedgreetings = ["Hello!","Hi!","Hey!","Heya!"]
    RandomGreetings = random.choice(Listedgreetings)
    await ctx.send(f"{RandomGreetings} I am Tornax a Multi-Talented Discord Bot, Designed, Created and Configured by MrinalSparks")

@client.command()
async def about(ctx):
    await ctx.send(f"Tornax is a Multi-Talented and Friendly Bot, Use Tornax for moderation, server managements, streams and giveaways now!")

@client.event
async def on_message(message):
    message.content = message.content.lower()
    for word in restricted_words:
        if message.content.count(word)>0:
            await message.channel.purge(limit = 1)
    await client.process_commands(message)

client.run(TOKEN)