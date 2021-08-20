import discord
from discord.ext import commands
from datetime import datetime
import random
from typing import Optional

bot = commands.Bot(command_prefix = ">")
restricted_words = ["gooh","kutta","kutte","harami","skyra","wtf","frick","fuck"]

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.yfzVgB8hHizDFH7hSMTORIv5weg"

@bot.event
async def on_ready():
    print("I m Ready!")

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

@bot.command()
async def ping(ctx, toping):
    try:
        if toping.startswith("@"):
            await ctx.send(f"{toping}")
        else:
            await ctx.send(f"@{toping}")
    except Exception:        
        await ctx.send(f"Please Specify the User Whom I have to Ping")

@bot.command()
async def time(ctx):
    currenttime = datetime.now()
    await ctx.send(f"Current Time is {currenttime}")
    
@bot.listen()
async def on_message(message):
    if ("smp" in message.content.lower() or "server" in message.content.lower()) and (" on " in message.content.lower() or "online" in message.content.lower() or "offline" in message.content.lower() or " off " in message.content.lower()):
        await message.channel.send(f"{message.author.mention} Please Check <#877777208108789770> for Live Updates of Smp")
        
@bot.command()
async def tell(ctx, channel: Optional[discord.TextChannel]=None, *, msg):
    if channel is None:
        channel = ctx.channel
    await channel.send(f"{msg}")

@bot.command()
async def rule(ctx, ruleno):
    if ruleno == "1":
        embed = discord.Embed(title="Rule No. 1 - No Promotion",description='Discord Server, Youtube, Website and other Promotions are not Allowed',color = discord.Color.from_rgb(255, 255, 0))
        await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, owner: Optional[discord.Member]=None):
    if owner is None:
        owner = ctx.author
    embed = discord.Embed(title="Avatar",color=discord.Color.from_rgb(255, 255, 0))
    embed.set_author(icon_url=owner.avatar_url,name=owner)
    embed.set_image(url=owner.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)


@bot.command()
async def commands(ctx):
    myEmbed = discord.Embed(title = 'Commands', description = "All Commands which you can use after using Tornax prefix '>'", color = discord.Color.from_rgb(255, 255, 0))
    myEmbed.add_field(name="hi", value="To get Reply From Tornax", inline=True)
    myEmbed.add_field(name="ping", value="To get Ping by Tornax", inline=True)
    myEmbed.add_field(name="tell", value="Chat something using Tornax", inline=False)
    myEmbed.add_field(name="time", value="Get Current Time", inline=True)
    await ctx.send(embed=myEmbed)

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
            await message.channel.send(f":exclamation: The Word you are Using is Not Allowed in this Server {message.author.mention}")
    await bot.process_commands(message)

bot.run(TOKEN)