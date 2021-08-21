import discord
from discord.ext import commands
from datetime import datetime
import random
from typing import Optional

bot = commands.Bot(command_prefix = ">")
restricted_words = ["gooh","kutta","kutte","harami","skyra","wtf","frick","fuck"]

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.yfzVgB8hHizDFH7hSMTORIv5weg"

embedTheme = discord.Color.from_rgb(255, 255, 0)

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
async def rule(ctx, ruleno: Optional[str]=None):
    if ruleno is None:
        await ctx.send(f":exclamation: Please Specify the Rule Number of the Rule which you want to Access,{ctx.author.mention}")
    else:
        if ruleno == "1":
            embed = discord.Embed(title="Rule No. 1 - No Promotion",description='Discord Server, Youtube, Website and other Promotions are not Allowed \n \n No type of Promotion is Allowed, Emotionally or Friendly Blackmailing to Subscribe, Like or to join a Discord Server or others is type of Promotion and You can get warn, mute or ban from the Server.   ',color = embedTheme)
            await ctx.send(embed=embed)
        elif ruleno == "2":
            embed = discord.Embed(title="Rule No. 2 - No Abuses",description="Abuses or any Kind of Abusing Languages are Not Allowed \n\n Abusing Words or even Targeting Someone's Family member is a kind of Abuse and you can get mute or ban from the Server.",color = embedTheme)
            await ctx.send(embed=embed)
        elif ruleno == "3":
            embed = discord.Embed(title="Rule No. 3 - No Spamming",description="Spamming is Restricted here even while crazy or angry \n\n We will not coperate any type of Spamming here even you can get warn or mute for that",color = embedTheme)
            await ctx.send(embed=embed)
        elif ruleno == "4":
            embed = discord.Embed(title="Rule No. 4 - No Toxicity",description='Toxic Behaviour with Server Staff or Member is Not Tolerated \n\n Toxicity or rudeness with the Members of this Server without any necessary reason after getting warning can give warn or mute',color = embedTheme)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f":exclamation: There is no Rule Number {ruleno},{ctx.author.mention}")
        
@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="Server Rules", description="These are some Rules of this Server", color= embedTheme)
    embed.add_field(name="1. No Promotion",value="  type >rule 1 for more info",inline= False)
    embed.add_field(name="2. No Abuses",value="  type >rule 2 for more info",inline= False)
    embed.add_field(name="3. No Spamming",value="  type >rule 3 for more info",inline= False)
    embed.add_field(name="4. No Toxicity",value="  type >rule 4 for more info\n\n",inline= False)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, owner: Optional[discord.Member]=None):
    if owner is None:
        owner = ctx.author
    embed = discord.Embed(title="Avatar",color=embedTheme)
    embed.set_author(icon_url=owner.avatar_url,name=owner)
    embed.set_image(url=owner.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)


@bot.command()
async def commands(ctx):
    myEmbed = discord.Embed(title = 'Commands', description = "These are all Commands, This Server prefix - '>' \n\n", color = embedTheme)
    myEmbed.add_field(name="hi", value="To get Reply From Tornax", inline=True)
    myEmbed.add_field(name="ping", value="To get Ping or Ping Someone by Tornax", inline=True)
    myEmbed.add_field(name="tell", value="Chat something and anywhere using Tornax", inline=True)
    myEmbed.add_field(name="time", value="Get Current Time", inline=True)
    myEmbed.add_field(name="avatar", value="See any Server member's Profile Picture", inline=True)
    myEmbed.add_field(name="rules", value="Get all Rules of the server", inline=True)
    myEmbed.add_field(name="Total Commands - 6", value="More Coming Soon", inline=False)
    myEmbed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.author}")
    await ctx.send(embed=myEmbed)

@bot.command()
async def info(ctx):
    Listedgreetings = ["Hello!","Hi!","Hey!","Heya!"]
    RandomGreetings = random.choice(Listedgreetings)
    await ctx.send(f"> {RandomGreetings} I am Tornax a Multi-Talented Discord Bot, Designed, Created and Configured by MrinalSparks")

@bot.command()
async def about(ctx):
    await ctx.send(f"> Tornax is a Multi-Talented and Friendly Bot, Use Tornax for moderation, server managements, streams and giveaways now!")

@bot.listen()
async def on_message(message):
    if "start" in message.content.lower() and "smp" in message.content.lower():
        await message.add_reaction(<:nahi:869447646866202624>)

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    for word in restricted_words:
        if message.content.count(word)>0:
            await message.channel.purge(limit = 1)
            await message.channel.send(f":exclamation: The Word you are Using is Not Allowed in this Server {message.author.mention}")
    await bot.process_commands(message)

bot.run(TOKEN)