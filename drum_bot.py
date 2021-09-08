import discord
from discord.ext import commands
from datetime import datetime
import random
from typing import Optional

from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MessageNotFound

bot = commands.Bot(command_prefix = ">")

restricted_words = ["gooh","kutta","kutte","harami","skyra","wtf","frick","fuck","fuk","tatti","baap","stfu"]

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.yfzVgB8hHizDFH7hSMTORIv5weg"

embedTheme = discord.Color.from_rgb(255, 255, 0)

@bot.event
async def on_ready():
    status = discord.Status.online
    activity = discord.Activity(type=discord.ActivityType.watching, name="Server Members | >help for commands")
    await bot.change_presence(status=status, activity=activity)
    print("I m Ready!")

###############
#### Only For My Smp Server
###############

SmpStatus = False
LegendServer = 869439705714933780

@bot.event
async def on_member_join(member):
    role1 = discord.utils.get(member.server.roles, id=875247780535345222)
    role2 = discord.utils.get(member.server.roles, id=875259339072491541)
    await bot.add_roles(member, role1)
    await bot.add_roles(member, role2)

@bot.listen()
async def on_message(message):
    if message.guild.id == LegendServer:
        if message.author.id != 832897602768076816:
            if ("smp" in message.content.lower() or "server" in message.content.lower()) and (" on " in message.content.lower() or "online" in message.content.lower() or "offline" in message.content.lower() or " off " in message.content.lower()):
                await message.channel.send(f"{message.author.mention} Please Check <#877777208108789770> for Live Updates of Smp")
        
@bot.command()
async def dmuser(ctx, member: discord.User, *, chat):
    if ctx.guild.id == LegendServer:
        if ctx.author.id == 758941956600102943:
            await member.send(chat)
        else:
            await ctx.send(f":exclamation: Sorry {ctx.author.mention}, You Don't have Acess to use this Command")

@bot.listen()
async def on_message(message):
    if message.guild.id == LegendServer:
        if message.channel == message.author.dm_channel:
            channelid = 874904257265008670
            modmail = bot.get_channel(channelid)
            embed = discord.Embed(title=f"{message.author}", color=embedTheme)
            embed.add_field(name="Message\n",value=f"{message.content}\n\n--------------------------",inline=False)
            embed.set_footer(icon_url=message.author.avatar_url,text=f"ID -> {message.author.id}")
            await modmail.send(embed=embed)
            # print(f"{message.author} -> {message.content}")

@bot.listen()
async def on_message(message):
    if message.guild.id == LegendServer:
        if "start" in message.content.lower() and "smp" in message.content.lower():
            await message.add_reaction("<:nahi:869447646866202624>")

@bot.listen()
async def on_message(message):
    global SmpStatus
    if message.guild.id == LegendServer:
        Smpchannel = bot.get_channel(877777208108789770)
        if message.channel == Smpchannel:
            if message.author.id == 832897602768076816:
                if "server has started" in message.content.lower():
                    SmpStatus = True
                    # print(f"Smp Status is {SmpStatus}")
                elif "server has stopped" in message.content.lower():
                    SmpStatus = False
                    # print(f"Smp Status is {SmpStatus}")

@bot.command()
async def status(ctx):
    if ctx.guild.id == LegendServer:
        if SmpStatus == True:
            await ctx.send(f":green_circle:  Server Is Online")
        elif SmpStatus == False:
            await ctx.send(f":red_circle:  Server Is Offline")

##############################
#### All Servers Commands ####
##############################

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member:discord.Member, *, reason=None):
    if member is not None:
        await ctx.send(f"Warned: {member.mention} has been Warned by {ctx.author.mention}" if reason is None else f"Warned: {member.mention} has been Warned by {ctx.author.mention} \n\t With the Reason of :\t{reason}")
    else:
        await ctx.send(f"You must Specify the User whom you want to Warn")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, reason=None):
    if member is not None:
        await member.kick(reason=reason)
        await ctx.send(f"Kicked: {member.mention} has been Kicked from the Server by {ctx.author.mention}" if reason is None else f"Kicked: {member.mention} has been Kicked from the Server by {ctx.author.mention} \n\t With the Reason of :\t{reason}")
    else:
        await ctx.send(f"You must Specify the User whom you want to Kick from the Server")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def leaveserver(ctx):
        await ctx.guild.leave()
        # await ctx.send(f"{ctx.author.mention} Sorry you don't have Access to use this Command")

@bot.command()
async def react(ctx, chat:Optional[discord.Message], emoji):
    if chat is None:
        await ctx.message.delete()
        chat = ctx.channel.last_message
        message = chat
        await message.add_reaction(emoji)

@bot.command()
async def solve(ctx, num1, operation, num2):
    try:
        if operation == "+":
            await ctx.send(f"{ctx.author.mention}  {num1} + {num2} = {num1 + num2}")
        elif operation == "-":
            await ctx.send(f"{ctx.author.mention}  {num1} - {operation}{num2} = {num1 - num2}")
        elif operation == "*" or operation.lower() == "x":
            await ctx.send(f"{ctx.author.mention}  {num1} x {num2} = {num1 * num2}")
        elif operation == "/" or operation == "÷":
            await ctx.send(f"{ctx.author.mention}  {num1} ÷ {num2} = {num1 / num2}")
    except:
        embed = discord.Embed(title="Command : >solve", description=f"Usage : >solve [Number1] [Operation: +,-,*,/] [Number2]",color=embedTheme)
        await ctx.send(embed=embed)

@bot.command()
async def ping(ctx, toping:Optional[discord.Member]=None):
    await ctx.message.delete()
    await ctx.send(toping.mention if toping is not None else ctx.author.mention)

@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def time(ctx):
    currenttime = datetime.now()
    await ctx.send(f"Current Time is {currenttime}")

@bot.command()
async def tell(ctx, channel: Optional[discord.TextChannel]=None, *, msg):
    if channel is None:
        channel = ctx.channel
    await channel.send(msg)

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
async def gethelp(ctx):
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
    message.content = message.content.lower()
    for word in restricted_words:
        if message.content.count(word)>0:
            await message.channel.purge(limit = 1)
            await message.channel.send(f":exclamation: The Word you are Using is Not Allowed in this Server {message.author.mention}")

bot.run(TOKEN)