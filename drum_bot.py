import discord
from discord.ext import commands
from datetime import datetime

client = commands.Bot(command_prefix = ">")
restricted_words = ["gooh","kutta","kutte","harami","skyra"]

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.G6KU_qx6QV1O2mSLEv9ncaBKM-Y"

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
async def on_message(message,ctx):
    message.content = message.content.lower()
    for word in restricted_words:
        if message.content.count(word)>0:
            await message.channel.purge(limit = 1)
    await client.process_commands(message)
    await ctx.send(f"The Word you are Using is not Allowed Here")

client.run(TOKEN)