from os import name
import warnings
import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import random
from typing import Optional
import json
import time
from mcstatus import MinecraftServer
import asyncpg
from PIL import Image, ImageDraw
from io import BytesIO
import wikipedia
from googlesearch import search
import topgg

from discord.ext.commands import has_permissions,has_role,MissingPermissions,MissingRole,CommandNotFound,CommandInvokeError, MissingAnyRole
from discord.member import Member


DEFAULT_PREFIX = ">"

async def load_prefix(bot, message):
    global DEFAULT_PREFIX
    if not message.guild:
        current_prefix = DEFAULT_PREFIX
    else:        
        current_prefix = await bot.pg_con.fetchrow("SELECT prefix FROM prefixes WHERE guild_id  = $1", message.guild.id)
        if not current_prefix:
            current_prefix = await bot.pg_con.execute("INSERT INTO prefixes(guild_id, prefix) VALUES($1,$2)", message.guild.id, DEFAULT_PREFIX)

    return current_prefix

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = load_prefix, case_insensitive=True, intents=intents,help_command=None)

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.yfzVgB8hHizDFH7hSMTORIv5weg"

embedTheme = discord.Color.from_rgb(255, 255, 0)

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(dsn="postgres://lhdqtzqtddynlu:2790afc4d8f12e15c72d767b4e5c9c9c2d52279b971b54d487bda9ad720bf159@ec2-100-24-169-249.compute-1.amazonaws.com:5432/ddt3h5kmtjdr1h")
    await bot.pg_con.execute("CREATE TABLE IF NOT EXISTS prefixes(guild_id bigint, prefix text)") 
    print("Connected Successfully To DataBase")


@bot.event
async def on_ready():
    status = discord.Status.online
    activity = discord.Activity(type=discord.ActivityType.watching, name="Server Members | >help for commands")
    await bot.change_presence(status=status, activity=activity)
    print("I m Ready!")

@bot.command()
async def setprefix(ctx, *, newPrefix:Optional[str]=None):
    if ctx.author.guild_permissions.administrator:
        if newPrefix is not None:
            custom_prefix = await bot.pg_con.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", ctx.guild.id)
            if not custom_prefix:
                await bot.pg_con.execute("INSERT INTO prefixes(guild_id,prefix) VALUES($1,$2)", ctx.guild.id, DEFAULT_PREFIX)
            await bot.pg_con.execute("UPDATE prefixes SET prefix=$1 WHERE guild_id=$2",newPrefix,ctx.guild.id)
            await bot.user.edit(nick=f"[{newPrefix}] Tornax")
            await ctx.send(f"The Prefix for this Server is Successfully Changed to {newPrefix}")
        else:
            await ctx.send(f"You Must Specify the New Prefix")
    else:
        await ctx.send(f"You don't have Permissions to do that")

setprefixhelp = "setprefix <New Bot Prefix>"

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            if "chat" in channel.name or "general" in channel.name:
                await channel.send(f'Hey there! Thanks for Adding me in {guild.name}, Type `>help` to get All about me')
    inviteChannel = bot.get_channel(890819215588741191)
    inviteEmbed = discord.Embed(title = "Joined!", description=f"{bot.user.mention} Just Joined {guild.name}", color=embedTheme)
    inviteEmbed.set_thumbnail(url=guild.icon_url)
    inviteEmbed.add_field(name="Guild Owner", value=f"<@{guild.owner_id}>",inline=False)
    inviteEmbed.add_field(name="Guild Members", value=f"<@{guild.member_count}>",inline=False)
    inviteEmbed.add_field(name="Guild ID", value=guild.id,inline=False)
    await inviteChannel.send(embed=inviteEmbed)

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if "welcome" in channel.name:
            created_at = member.created_at.strftime("%a, %d %b %Y %I:%M %p")
            joined_at = member.joined_at.strftime("%a, %d %b %Y %I:%M %p")
            welcomeEmbed = discord.Embed(title="Welcome!", description=f"A Member Just Joined **{member.guild.name}**",color=embedTheme)
            welcomeEmbed.set_thumbnail(url=member.avatar_url)
            welcomeEmbed.add_field(name="Member Joined", value=f"{member.mention}",inline=True)
            welcomeEmbed.add_field(name="Member Id", value=f"{member.id}", inline=True)
            welcomeEmbed.add_field(name="Joined Discord", value=f"{created_at}", inline=False)
            welcomeEmbed.add_field(name=f"Joined {member.guild.name}", value=f"{joined_at}", inline=True)
            welcomeEmbed.add_field(name=f"Member Number", value=f"#{member.guild.member_count}", inline=True)
            await channel.send(embed=welcomeEmbed)
            await member.send(f"We Are So Excited to have you on {member.guild.name}")

@bot.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if "bye" in channel.name:
            byeEmbed = discord.Embed(title=f"**{member}** Just Left {member.guild.name}!",color=embedTheme)
            await channel.send(embed=byeEmbed)

@bot.event
async def on_dbl_vote(data):
    print(data)
    voteEmbed = discord.Embed(title="Voted!", description=f"{data}",color=embedTheme)
    # voteEmbed.add_field(name=f"Voter ID", value=f"{user.id}", inline=False)
    voteAnnounce = bot.get_channel(892260693846401054)
    # await user.send(f"Thanks For Voting {bot.user.mention} !! You Can get Rewards in Our Official Server - [Join](https://discord.gg/H3688EEpWr) ")
    await voteAnnounce.send(embed=voteEmbed)

###############
#### Only For My Smp Server
###############

SmpStatus = False
LegendServer = 869439705714933780
Creater = "MrinalSparks#8633"
        
@bot.command()
async def dmuser(ctx, member: discord.User, *, chat):
    if ctx.guild.id == LegendServer:
        if ctx.author.id == 758941956600102943:
            await member.send(chat)
        else:
            await ctx.send(f":exclamation: Sorry {ctx.author.mention}, You Don't have Access to use this Command")

@bot.listen()
async def on_message(message):
    if not message.guild:
        channelid = 874904257265008670
        modmail = bot.get_channel(channelid)
        embed = discord.Embed(title=f"{message.author}", color=embedTheme)
        embed.add_field(name="Message\n",value=f"{message.content}\n\n--------------------------",inline=False)
        embed.set_footer(icon_url=message.author.avatar_url,text=f"ID -> {message.author.id}")
        await modmail.send(embed=embed)
        # print(f"{message.author} -> {message.content}")

@bot.listen()
async def on_message(message):
    global SmpStatus
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
############0##################

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, days: Optional[int]=None, *, reason:Optional[str]=None):
    try:
        memberId = member.id
        if days is not None:
            wait = days * 86400
            if not member.guild_permissions.administrator:
                embed = discord.Embed(description = f"** {member.mention} has been Banned Successfully by {ctx.author.mention} for `{days}` Days **" if reason is None else f"** {member.mention} has been Banned Successfully by {ctx.author.mention} for `{days}` Days \n\t With the Reason of :\t{reason}**",color=embedTheme)
                dmuser = discord.Embed(description = f"** You are Banned by an Admin from {ctx.guild.name} for `{days}` Days **" if reason is None else f"** You are Banned by an Admin from {ctx.guild.name} for `{days}` Days \n\t With the Reason of :\t{reason}**",color=embedTheme)
                await ctx.send(embed=embed)
                await member.send(embed=dmuser)
                await member.ban(reason=reason)
                await asyncio.sleep(wait)
                await ctx.guild.unban(memberId)
            else:
                await ctx.reply(f":exclamation: You Cannot Ban an Admin")
        else:
            if not member.guild_permissions.administrator:
                embed = discord.Embed(description = f"** {member.mention} has been Banned Successfully by {ctx.author.mention} **" if reason is None else f"** {member.mention} has been Banned Successfully by {ctx.author.mention} \n\t With the Reason of :\t{reason}**",color=embedTheme)
                dmuser = discord.Embed(description = f"** You are Banned by an Admin from {ctx.guild.name} **" if reason is None else f"** You are Banned by an Admin from {ctx.guild.name} \n\t With the Reason of :\t{reason}**",color=embedTheme)
                await ctx.send(embed=embed)
                await member.send(embed=dmuser)
                await member.ban(reason=reason)
            else:
                await ctx.reply(f":exclamation: You Cannot Ban an Admin")
    except Exception as e:
        print(e)
        await ctx.reply(f":exclamation: You don't have Permissions to do that!")

banhelp = f"ban <member> [days] [reason]"

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id:int):
    global embedContent
    try:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        embedContent = f"Unbanned : Successfully Unbanned {user} from {ctx.guild.name}"
        embed = discord.Embed(description=embedContent, color=embedTheme)
        await ctx.send(embed=embed)
    except MissingPermissions and Exception as e:
        print(e)
        await ctx.send(f":exclamation: {ctx.author.mention} You don't have Permissions to do that")

unbanhelp = f"unban <member id>"

@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member:discord.Member, duration: Optional[int]=None, unit: Optional[str]=None, *, reason: Optional[str]=None ):
    try:
        try:
            if duration is None and unit is not None:
                reason = unit
                unit = None
            mutedRole = discord.utils.get(ctx.message.guild.roles, name="Muted")
            if not mutedRole:
                mutedRole = await ctx.guild.create_role(name="Muted")

                for channel in ctx.guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
            if duration is not None and unit is not None:
                if unit == "s" or "sec" in unit:
                    wait = 1 * duration 
                    embed = discord.Embed(description = f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Seconds **" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Seconds \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    dmAlert = f"You are Muted in the Server by an Admin for `{duration}` Seconds"if reason is None else f"You are Muted in the Server by an Admin for `{duration}`` Seconds\n\t With the Reason of {reason}"
                elif unit == "m" or "min" in unit:
                    wait = 60 * duration 
                    embed = discord.Embed(description = f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Minutes **" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Minutes \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    dmAlert = f"You are Muted in the Server by an Admin for `{duration}` Minutes"if reason is None else f"You are Muted in the Server by an Admin for `{duration}`` Minutes\n\t With the Reason of {reason}"
                elif unit == "h" or unit == "hour":
                    wait = 60 * 60 * duration 
                    embed = discord.Embed(description = f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Hours **" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Hours \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    dmAlert = f"You are Muted in the {ctx.guild.name} Server by an Admin for `{duration}` Hours"if reason is None else f"You are Muted in the {ctx.guild.name} Server by an Admin for `{duration}`` Hours\n\t With the Reason of {reason}"
                if not member.guild_permissions.administrator:
                    await member.add_roles(mutedRole)
                    await ctx.send(embed=embed,delete_after=15)
                    await member.send(dmAlert)
                    await asyncio.sleep(wait)
                    await member.remove_roles(mutedRole)
                else:
                    await ctx.reply(f":exclamation: You Cannot Mute an Admin")
            else:
                if not member.guild_permissions.administrator:
                    embed = discord.Embed(description=f"** {member.mention} has been Muted Successfully by {ctx.author.mention}**" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention}\n\t With the Reason of :\t{reason}**",color=embedTheme)
                    await member.add_roles(mutedRole)
                    await ctx.send(embed=embed,delete_after=15)
                    await member.send(f"You are Muted in the Server by an Admin"if reason is None else f"You are Muted in the Server by an Admin\n\t With the Reason of {reason}")
                else:
                    await ctx.reply(f":exclamation: You Cannot Mute an Admin")
        except Exception:
            pass
    except MissingPermissions:
        await ctx.reply(f":exclamation: You don't have Permissions to do that!")

mutehelp = f"mute <member> [duration] [unit = s,m,h] [reason]"

@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member:discord.Member, *, reason: Optional[str]=None):
    mutedRole = discord.utils.get(ctx.message.guild.roles, name="Muted")
    if mutedRole in member.roles:
        embed = discord.Embed(description=f"** {member.mention} has been Unmuted Successfully by {ctx.author.mention}**" if reason is None else f"** {member.mention} has been Unmuted Successfully by {ctx.author.mention}\n\t With the Reason of :\t{reason}**",color=embedTheme)
        await member.remove_roles(mutedRole)
        await ctx.send(embed=embed,delete_after=15)
    else:
        embed = discord.Embed(description=f"** :exclamation: {member.mention} is Not Muted in this Server **",color=embedTheme)
        await ctx.send(embed=embed,delete_after=15)

unmutehelp = f"unmute <member> [reason]"

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member:discord.Member, *, reason=None):
    if member is not None:
        await ctx.send(f"Warned: {member.mention} has been Warned by {ctx.author.mention}" if reason is None else f"Warned: {member.mention} has been Warned by {ctx.author.mention} \n\t With the Reason of :\t{reason}")
        await member.send(f"You are Warned by an Admin in {ctx.guild.name}"if reason is None else f"You are Warned by an Admin in {ctx.guild.name} \n\t With the Reason of :\t{reason}")
    else:
        await ctx.send(f"You must Specify the User whom you want to Warn")

warnhelp = f"warn <member> [reason]"

@warn.error
async def warn_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, reason=None):
    if member is not None:
        if member == ctx.author:
            await ctx.send(f":exclamation: You cannot Kick yourself {ctx.author.mention}")
        else:
            if not member.guild_permissions.administrator:
                await member.kick(reason=reason)
                await ctx.send(f"Kicked: {member.mention} has been Kicked from the Server by {ctx.author.mention}" if reason is None else f"Kicked: {member.mention} has been Kicked from the Server by {ctx.author.mention} \n\t With the Reason of :\t{reason}")
                await member.send(f"You are Kicked by an Admin from {ctx.guild.name}"if reason is None else f"You are Kicked by an Admin from {ctx.guild.name} \n\t With the Reason of :\t{reason}")
            else:
                await ctx.reply(f":exclamation: You Cannot Kick an Admin")
    else:
        await ctx.send(f"You must Specify the User whom you want to Kick from the Server")

kickhelp = f"kick <member> [reason]"

@kick.error
async def kick_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

leaveConfirmation = 0
leavingRequest = {}

@bot.command()
@commands.has_permissions(manage_guild=True)
async def leaveserver(ctx):
    global leaveConfirmation, leavingRequest
    try:
        if ctx.guild.id not in leavingRequest:
            leavingRequest[ctx.guild.id] = ""
        leavingRequest[ctx.guild.id] = ctx.author.id
        await ctx.send(f"{ctx.author.mention} Do You Really Want me to Leave {ctx.guild.name} Server \:( , Send - Yes or No")
        leaveConfirmation = 20
        await asyncio.sleep(20)
        if leaveConfirmation == 20:
            await ctx.send(f"{ctx.author.mention} Your Replying/Answering Time Ended!")
            leaveConfirmation = 0
    except Exception as e:
        print(e)
        await ctx.send(f"{ctx.author.mention} Sorry you don't have Access to use this Command")

leaveserverhelp = f"leaveserver"

@bot.listen()
async def on_message(message):
    global leaveRequest, leaveConfirmation
    if message.guild.id not in leavingRequest:
            leavingRequest[message.guild.id] = ""

    if leaveConfirmation == 20:
        if message.author.id == leavingRequest[message.guild.id]:
            if message.content.lower() == "yes":
                await message.channel.send(f"{message.author.mention} Successfully Left Your Server Bye Bye! :(")
                await message.guild.leave()
            elif message.content.lower() == "no":
                await message.channel.send(f"Thank You So Much :) for Keeping me in {message.guild.name} Server")
                leaveConfirmation = 0
                del leavingRequest[message.guild.id]
        else:
            pass

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: Optional[discord.Member]=None, *, newname):
    if member is None:
        member = ctx.author
    membername = member.name
    await member.edit(nick=newname)
    embed = discord.Embed(title=f" _Done_ : {membername}'s Nickname has Changed to {newname} Successfully! ", color=embedTheme)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed, delete_after=15)

setnickhelp = f"setnick [member] <newname>"

@setnick.error
async def setnick_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def resetnick(ctx, member: Optional[discord.Member]=None):
    if member is None:
        member = ctx.author
    membername = member.name
    await member.edit(nick=None)
    embed = discord.Embed(title=f" _Done_ : {membername}'s Nickname has Removed Successfully! ", color=embedTheme)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed, delete_after=15)

resetnickhelp = f"resetnick [member]"

@resetnick.error
async def resetnick_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit:int):
    if limit > 0:
        quantity = "Messages"
        if limit == 1:
            quantity = "Message"
        await ctx.channel.purge(limit=limit+1)
        embed = discord.Embed(title=f"🗑️   Successfully Deleted {limit} {quantity} from this Channel", color=embedTheme)
        await ctx.send(embed=embed,delete_after=8)
    else:
        embed = discord.Embed(title=f"Nothing Deleted from this Channel", color=embedTheme)
        await ctx.send(embed=embed,delete_after=8)    

cleanhelp = f"clean <limit>"

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: Optional[discord.TextChannel]=None):
    if channel is None:
        channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages=False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(description=f"** Locked : {channel.mention} has been Locked by {ctx.author.mention} **", color=embedTheme)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

lockhelp = f"lock [channel]"

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: Optional[discord.TextChannel]=None):
    if channel is None:
        channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages=True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(description=f"** Unlocked : {channel.mention} has been Unlocked by {ctx.author.mention} **", color=embedTheme)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

unlockhelp = f"unlock [channel]"

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: Optional[str]=None):
    try:
        if seconds is not None:
            if seconds.lower() == "off":
                seconds = 0
            await ctx.channel.edit(slowmode_delay=int(seconds))
            embed = discord.Embed(description=f"{ctx.author.mention} Successfully Set Slowmode to `{seconds}`", color=embedTheme)
            await ctx.send(embed=embed, delete_after=10)
        else:
            await ctx.send(f":exclamation: {ctx.author.mention} Please Specify the delay of the Slowmode")
    except Exception as e:
        print(e)
        await ctx.send(f":exclamation: {ctx.author.mention} You don't have Permissions to do that")

slowmodehelp = f"slowmode <seconds>"

@bot.command()
async def thought(ctx, *, word):
    if " " in word:
        word = discord.Embed(description=f"You cannot use More than one Word",color=embedTheme)
        await ctx.send(embed=word,delete_after=8)
    else:
        embed = discord.Embed(title=f"\t{word.upper()}", color=embedTheme)
        await ctx.send(embed=embed)

thoughthelp = f"thought <word>"

class Giveaway():
    global GiveawayActive
    global GiveawayChannel
    global StartAnnounce
    global ParticipantsMsg
    global MembersList
    global Participants
    GiveawayActive = {}
    GiveawayChannel = {}

    StartAnnounce = {}
    ParticipantsMsg = {}
    MembersList = {}

    Participants = {

    }

    @bot.command()
    async def gstart(ctx, Channel:discord.TextChannel, prize:str, endtime:int, unit:str):
        global GiveawayActive, GiveawayChannel, StartAnnounce, MembersList, ParticipantsMsg
        GiveawayRole = discord.utils.get(ctx.guild.roles, name="Giveaway Handler")
        if GiveawayRole in ctx.author.roles:
            if ctx.guild.id not in GiveawayActive:
                GiveawayActive[ctx.guild.id] = False
            if ctx.guild.id not in Participants:
                Participants[ctx.guild.id] = {}
            if ctx.guild.id not in MembersList:
                MembersList[ctx.guild.id] = ""
            if ctx.guild.id not in ParticipantsMsg:
                ParticipantsMsg[ctx.guild.id] = ""

            if GiveawayActive[ctx.guild.id] == False:
                GiveawayActive[ctx.guild.id] = True
                GiveawayChannel[ctx.guild.id] = Channel
                listtostr = list(Participants[ctx.guild.id].keys())
                members = str(listtostr)

                members = members.replace("'","") 
                members = members.replace("[","") 
                members = members.replace("]","")
                # await asyncio.sleep(int(endtime))

                if GiveawayActive[ctx.guild.id] ==True:
                    if unit == "s" or "sec" in unit:
                        wait = 1 * endtime
                        unitTime = "Seconds"
                    elif unit =="m" or "min" in unit:
                        wait = 60 * endtime
                        unitTime = "Minutes"
                    elif unit == "h" or unit == "hours":
                        wait = 60 * 60 * endtime
                        unitTime = "Hours"

                    StartAnnounce[ctx.guild.id] = await ctx.send(f":loudspeaker:  Giveaway has been Started by {ctx.author.mention} and Will End After `{endtime}` {unitTime} :partying_face:")
                    ParticipantsMsg[ctx.guild.id] = await ctx.send(f":busts_in_silhouette: Participants - {MembersList[ctx.guild.id]}")

                if GiveawayActive[ctx.guild.id] == True:
                    await asyncio.sleep(wait)

                if GiveawayActive[ctx.guild.id] == True:
                    if len(Participants[ctx.guild.id]) == 0:
                        Participants[ctx.guild.id]["No One"] = "No one Participated"
                    winnerCode = random.choice(list(Participants[ctx.guild.id].values()))
                    CodeOwner = [k for k, v in Participants[ctx.guild.id].items() if v == winnerCode]
                    # print(CodeOwner)
                    winnerName = str(CodeOwner[0])
                    winner = f"{winnerName} || {winnerCode}"

                    embed = discord.Embed(title=f":loudspeaker: Giveaway has been Finished :exclamation: :partying_face:\t ||{ctx.message.guild.default_role}||\n",color=embedTheme)
                    embed.add_field(name="Winner of the Giveaway",value=f"{winner}",inline=True)
                    embed.add_field(name="Prize",value=f"{prize}",inline=True)
                    embed.add_field(name="Participants",value=f"{MembersList[ctx.guild.id]}\n\n Please Contact with The Giveaway Players For the Prize of this Giveaway",inline=False)

                    await GiveawayChannel[ctx.guild.id].send(embed=embed)
                    Participants[ctx.guild.id].clear()
                    MembersList[ctx.guild.id] = ""
                    GiveawayActive[ctx.guild.id] = False
                    GiveawayChannel[ctx.guild.id] = None
            else:
                await ctx.send(":exclamation: A Giveaway is Already Active in this Server")
        else:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}, use `>help gstart` for more help')

    @bot.command()
    async def gparticipate(ctx):
        global StartAnnounce, MembersList, ParticipantsMsg
        if ctx.guild.id not in GiveawayActive:
                GiveawayActive[ctx.guild.id] = False
        if GiveawayActive[ctx.guild.id] == True:
            if ctx.channel == GiveawayChannel[ctx.guild.id]:
                if ctx.author.name not in Participants[ctx.guild.id]:
                    code = random.randint(000000,999999)
                    if code in Participants[ctx.guild.id]:
                        code = random.randint(000000,999999)
                    Participants[ctx.guild.id][ctx.author.name] = code

                    listtostr = list(Participants[ctx.guild.id].keys())
                    members = str(listtostr)

                    members = members.replace("'","")
                    members = members.replace("[","")
                    members = members.replace("]","")
                    MembersList[ctx.guild.id] = members

                    await ctx.author.send(f":partying_face: You have Successfully Participated in the Giveaway and Your Special Code for The Giveaway is `{code}`")
                    await ctx.send(f"{ctx.author.mention} We Accepted your Request, Please Check your Dm", delete_after=15)
                    await ParticipantsMsg[ctx.guild.id].edit(content=f":busts_in_silhouette: Participants - {MembersList[ctx.guild.id]}")
                else:
                    await ctx.send(f"{ctx.author.mention} You have Already Participated in the Giveaway, you cannot Participate again", delete_after=15)
        else:
            await ctx.send(":exclamation: There is No Giveaway Active in this Server")

    @bot.command()
    async def gquit(ctx):
        global StartAnnounce, MembersList, ParticipantsMsg
        if ctx.guild.id not in GiveawayActive:
                GiveawayActive[ctx.guild.id] = False
        if GiveawayActive[ctx.guild.id] == True:
            if ctx.channel == GiveawayChannel[ctx.guild.id]:
                if ctx.author.name in Participants[ctx.guild.id]:

                    del Participants[ctx.guild.id][ctx.author.name]

                    listtostr = list(Participants[ctx.guild.id].keys())
                    members = str(listtostr)

                    members = members.replace("'","") 
                    members = members.replace("[","") 
                    members = members.replace("]","")
                    MembersList[ctx.guild.id] = members

                    await ctx.send(f"{ctx.author.mention} You have Successfully Quitted the Giveaway", delete_after=15)
                    await ParticipantsMsg[ctx.guild.id].edit(content=f":busts_in_silhouette: Participants - {MembersList[ctx.guild.id]}")
                else:
                    await ctx.send(f"{ctx.author.mention} You are Already not a Participant of this Giveaway", delete_after=15)
        else:
            await ctx.send(":exclamation: There is No Giveaway Active in this Server")
    
    @bot.command()
    async def gstatus(ctx):
        GiveawayRole = discord.utils.get(ctx.guild.roles, name="Giveaway Handler")
        if GiveawayRole in ctx.author.roles:
            if ctx.guild.id not in GiveawayActive:
                GiveawayActive[ctx.guild.id] = False
            if GiveawayActive[ctx.guild.id]:
                await ctx.send(f"A Giveaway is Currently Active in this Server \n Number of Participants :- {Participants[ctx.guild.id]}\n Giveaway Channel :- {GiveawayChannel[ctx.guild.id]}")
            else:
                await ctx.send(":exclamation: There is No Giveaway Active in this Server")
        else:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}, use `>help gstatus` for more help')

    @bot.command()
    async def gstop(ctx):
        global GiveawayActive, Participants, GiveawayChannel, MembersList
        GiveawayRole = discord.utils.get(ctx.guild.roles, name="Giveaway Handler")
        if GiveawayRole in ctx.author.roles:
            if ctx.guild.id not in GiveawayActive:
                GiveawayActive[ctx.guild.id] = False
            if GiveawayActive[ctx.guild.id] == True:
                GiveawayActive[ctx.guild.id] = False
                GiveawayChannel[ctx.guild.id] = None
                Participants[ctx.guild.id].clear()
                MembersList[ctx.guild.id] = ""
                await ctx.send(f"Giveaway has been Stopped by {ctx.author.mention}")
            else:
                await ctx.send(":exclamation: There is No Giveaway Active in this Server")
        else:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}, use `>help gstop` for more help')

gstarthelp = f"gstart <channel> <prize> <endtime> <unit , for ex:- s,m,h>"
gstophelp = f"gstop"
gparticipatehelp = f"gparticipate"
gquithelp = f"gquit"
gstatushelp = f"gstatus"

@bot.command()
async def react(ctx, chat:Optional[discord.Message], emoji):
    message = chat
    await message.add_reaction(emoji)

reacthelp = f"react <message id> <emoji>"

@bot.command()
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        try:
            await channel.connect()
        except:
            await ctx.send(f":exclamation: {ctx.author.mention} Tornax is Already Connected to a Voice Channel!")
    except CommandInvokeError:
        await ctx.send(f":exclamation: {ctx.author.mention} You must be in a Voice Channel to do that!")

joinhelp = f"join"

@bot.command()
async def leave(ctx):
    try:
        try:
            await ctx.voice_client.disconnect()
        except:
            await ctx.send(f":exclamation: {ctx.author.mention} Tornax is Not Connected to any Voice Channel!")
    except CommandInvokeError:
        await ctx.send(f":exclamation: {ctx.author.mention} You must be in a Voice Channel to do that!")

leavehelp = f"leave"

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: Optional[discord.Member]=None, role: discord.Role=None):
    if member is None:
        member = ctx.author
    if role in member.roles:
        embed = discord.Embed(description=f"** :exclamation: {member.mention} Already have {role.mention} Role **", color=embedTheme)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
        await ctx.send(embed=embed, delete_after=8)
    else:
        await member.add_roles(role)
        embed = discord.Embed(description=f"** Successfully Added {role.mention} Role to {member.mention} **", color=embedTheme)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
        await ctx.send(embed=embed, delete_after=8)

addrolehelp = f"addrole [member] <role>"

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: Optional[discord.Member]=None, role: discord.Role=None):
    if member is None:
        member = ctx.author
    if role in member.roles:
        await member.remove_roles(role)
        embed = discord.Embed(description=f"** Successfully Removed {role.mention} Role from {member.mention} **", color=embedTheme)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
        await ctx.send(embed=embed, delete_after=8)
    else:
        embed = discord.Embed(description=f"** :exclamation: {member.mention} Doesn't have {role.mention} Role **", color=embedTheme)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
        await ctx.send(embed=embed, delete_after=8)

removerolehelp = f"removerole [member] <role>"

@bot.command()
async def solve(ctx, num1, operation, num2):
    try:
        if "." in num1:
            num1 = float(num1)
        else:
            num1 = int(num1)
        if "." in num2:
            num2 = float(num2)
        else:
            num2 = int(num2)
        if operation == "+":
            await ctx.send(f"{ctx.author.mention}  {num1} + {num2} = {num1 + num2}")
        elif operation == "-":
            await ctx.send(f"{ctx.author.mention}  {num1} - {operation}{num2} = {num1 - num2}")
        elif operation == "*" or operation.lower() == "x" or operation == "×":
            await ctx.send(f"{ctx.author.mention}  {num1} × {num2} = {num1 * num2}")
        elif operation == "/" or operation == "÷":
            await ctx.send(f"{ctx.author.mention}  {num1} ÷ {num2} = {num1 / num2}")
    except:
        server_prefix = await bot.pg_con.fetchrow("SELECT prefix FROM prefixes WHERE guild_id  = $1", ctx.guild.id)
        embed = discord.Embed(title=f"Command : {ctx.prefix}solve", description=f"Usage : {ctx.prefix}solve [Number1] [Operation: +,-,*,/] [Number2]",color=embedTheme)
        await ctx.send(embed=embed)

solvehelp = f"solve <number1> <operation = +,-,×,÷> <number2>"

timer = {}
timerMsg = {}

@bot.command()
async def timerstart(ctx, seconds:int, *, reason: Optional[str]=None):
    global timer
    if ctx.guild.id not in timer:
        timer[ctx.guild.id] = False
    if timer[ctx.guild.id] == False:
        timer[ctx.guild.id] = True
        timerMsg[ctx.guild.id] = await ctx.send(f"Timer has Started : `{seconds}`"if reason is None else f"{reason} `{seconds}`")
        while 0 < seconds < seconds+1:
            if timer[ctx.guild.id] == True:
                await asyncio.sleep(0.7)
                seconds-=1
                await timerMsg[ctx.guild.id].edit(content=f"Timer has Started : `{seconds}`"if reason is None else f"{reason} `{seconds}`")
            else:
                break
        await asyncio.sleep(1)
        if timer[ctx.guild.id] == True:
            await timerMsg[ctx.guild.id].edit(content=f"Timer has Stopped {ctx.author.mention}")
            timer[ctx.guild.id] = False
        else:
            await timerMsg[ctx.guild.id].edit(content=f"Timer has Stopped {ctx.author.mention}")

    else:
        await ctx.send(f":exclamation: {ctx.author.mention} A Timer is already Running in this Server")

timerstarthelp = f"timerstart <seconds> [reason]"

@bot.command()
async def timerstop(ctx):
    global timer
    if ctx.guild.id not in timer:
        timer[ctx.guild.id] = False
    if timer[ctx.guild.id] == True:
        timer[ctx.guild.id] = False
        await timerMsg[ctx.guild.id].edit(content=f"Timer has Stopped by {ctx.author.mention}")
    else:
        await ctx.send(f":exclamation: {ctx.author.mention} Currently No Timer is Running in this Server")

timerstophelp = f"timerstop"

@bot.command()
async def ping(ctx):
    msg = await ctx.send(f"Pong!")
    await msg.edit(content = f"Pong! Latency is `{round(bot.latency * 1000 + 100)}ms`")

pinghelp = f"ping"

@bot.command()
async def invite(ctx):
    inviteEmbed = discord.Embed(title="Invite Tornax", description="Hey! Invite Tornax Now to Your Server For Server Management, Moderation, Auto Moderation and Fun\n\n[Invite Now](https://discord.com/api/oauth2/authorize?client_id=832897602768076816&permissions=536870911991&scope=bot)", color=embedTheme)
    inviteEmbed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=inviteEmbed)

invitehelp = f"invite"

@bot.command()
async def mcserver(ctx, server: Optional[str]=None):
    try:
        if server is not None:
            if "." in server:
                mcServer = MinecraftServer.lookup(server)
                status = mcServer.status()
                mcEmbed = discord.Embed(title=f"Looking For {server}", color=embedTheme)
                mcEmbed.add_field(name="Players Online", value=f"{status.players.online}", inline = False)
                mcEmbed.add_field(name="Server Pings", value=f"`{round(status.latency)}ms`", inline = False)
                mcEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author}")
                await ctx.send(embed=mcEmbed)
            else:
                await ctx.reply("You can Search a Server by its Ip not by Name")
        else:
            await ctx.reply("You Must Specify the Server Whose Detail You want to See")
    except Exception as e:
        print(e)
        await ctx.reply(f"The Server You are Looking For Does Not Exist, Recheck The Server IP")

mcserverhelp = f"mcserver <Minecaft Java Server Ip>"

@bot.command()
async def wikipedia(ctx, *, search: Optional[str]=None):
    try:
        if search is not None:
            query = wikipedia.summary(search, sentences=2)
            result = discord.Embed(title="Wikipedia", color=embedTheme)
            result.add_field(name=f"Search Results for {search}", value=f"{query}")
            result.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/220px-Wikipedia-logo-v2.svg.png")
            result.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author}")
            await ctx.send(embed=result)
        else:
            await ctx.reply(f"You Must Specify What you want to Search!")
    except:
        await ctx.reply(f"Something Went Wrong! We Didn't Found a Result for {search}")

wikipediahelp = f"wikipedia <Search Topic>"

@bot.command()
async def google(ctx, *, query):
    result = search(query, num_results=10, lang="en", proxy=None)
    finalresult = []
    for r in result:
        if not r.startswith("https"):
            result.remove(r)
    for rt in result:
        finalresult.append(f"• {rt}")

    totalresult = len(finalresult)
    finalresult = " \n ".join(finalresult)
    print(finalresult)
    googleEmbed = discord.Embed(title="Google Results", color=embedTheme)
    googleEmbed.set_thumbnail(url="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png")
    googleEmbed.add_field(name=f"Results For {query} - {totalresult}", value=f"{finalresult}", inline=False)
    googleEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author}")
    await ctx.send(embed=googleEmbed)

googlehelp = f"google <Search Topic>"

@bot.command()
async def time(ctx):
    currenttime = datetime.now()
    await ctx.send(f"Current Time is {currenttime}")

timehelp = f"time"

@bot.command()
async def tell(ctx, channel: Optional[discord.TextChannel]=None, *, msg):
    if channel is None:
        channel = ctx.channel
    if ctx.author.guild_permissions.administrator:
        await channel.send(msg)
    else:
        await ctx.reply(f"You don't have Permissions to do that, Only Admins Can Use the Command")

tellhelp = f"tell [channel] <message>"

active = {}
gamingChannel = {}

@bot.command()
async def guess(ctx):
    global active
    if ctx.guild.id not in active:
        active[ctx.guild.id] = False
    if ctx.guild.id not in gamingChannel:
        gamingChannel[ctx.guild.id] = {}

    if active[ctx.guild.id] == False:
        active[ctx.guild.id] = True
        gamingChannel[ctx.guild.id]["channel"] = ctx.channel
        randomRange = [0,10,20,30,40,50,60,70,80,90]
        gamingChannel[ctx.guild.id]["anyoneRange"] = random.choice(randomRange)
        gamingChannel[ctx.guild.id]["customRange"] = gamingChannel[ctx.guild.id]["anyoneRange"] + 20
        gamingChannel[ctx.guild.id]['secretNumber'] = random.randint(gamingChannel[ctx.guild.id]["anyoneRange"],gamingChannel[ctx.guild.id]["customRange"])
        print(gamingChannel[ctx.guild.id]['secretNumber'])
        gamingChannel[ctx.guild.id]["countdown"] = 20
        gamingChannel[ctx.guild.id]["guessed"] = False

        await ctx.send(f"🔢 Guess The Number Game #️⃣")
        gamingChannel[ctx.guild.id]["start"] = await ctx.send(f"I Challenge You to Guess the Number between {gamingChannel[ctx.guild.id]['anyoneRange']} to {gamingChannel[ctx.guild.id]['customRange']} in `{str(gamingChannel[ctx.guild.id]['countdown'])}` Seconds")
        gamingChannel[ctx.guild.id]["hidden"] = await ctx.send(f"➡️ ⬛ ⬅️")
        while gamingChannel[ctx.guild.id]["countdown"] > 0:
            await asyncio.sleep(0.7)
            gamingChannel[ctx.guild.id]["countdown"] -=1
            await gamingChannel[ctx.guild.id]["start"].edit(content=f"I Challenge You to Guess the Number between {gamingChannel[ctx.guild.id]['anyoneRange']} to {gamingChannel[ctx.guild.id]['customRange']} in `{str(gamingChannel[ctx.guild.id]['countdown'])}` Seconds")

        await gamingChannel[ctx.guild.id]["hidden"].edit(content=f"➡️ `{gamingChannel[ctx.guild.id]['secretNumber']}` ⬅️")    
        if gamingChannel[ctx.guild.id]["guessed"] == False:
            await ctx.send(f"Ha Ha! I Won the Challenge No one Guessed Correct >:)")
        active[ctx.guild.id] = False
    else:
        await ctx.reply(f"A Guess The Number Game is Already Active in this Server")

guesshelp = f"guess"

@bot.listen()
async def on_message(message):
    global active, gamingChannel
    if message.guild.id not in active:
        active[message.guild.id] = False
    try:
        if message.author.id not in gamingChannel[message.guild.id]:
            gamingChannel[message.guild.id][message.author.id] = {}
            gamingChannel[message.guild.id][message.author.id]["attempts"] = 0
        if message.author != bot.user:
            if active[message.guild.id] == True:
                if message.channel == gamingChannel[message.guild.id]["channel"]:
                    guesses = int(message.content)
                    if guesses > gamingChannel[message.guild.id]['secretNumber']:
                        await message.reply(f"Try a Smaller Number")
                        gamingChannel[message.guild.id][message.author.id]["attempts"] += 1
                    elif guesses < gamingChannel[message.guild.id]['secretNumber']:
                        await message.reply("Try a Bigger Number")
                        gamingChannel[message.guild.id][message.author.id]["attempts"] += 1
                    elif guesses == gamingChannel[message.guild.id]['secretNumber']:
                        gamingChannel[message.guild.id][message.author.id]["attempts"] += 1
                        await message.reply(f"{message.author.mention} You Guessed Correct in {gamingChannel[message.guild.id][message.author.id]['attempts']} Attempts and Won the Challenge, the Secret Number was `{gamingChannel[message.guild.id]['secretNumber']}`")
                        gamingChannel[message.guild.id]["guessed"] = True
                        gamingChannel[message.guild.id]["countdown"] = 1
                        del gamingChannel[message.guild.id]
    except Exception as e:
        print(e)
        pass

matches = {}
gameBoards = {}
chances = {}
teamCode = {}

@bot.command()
async def tictactoe(ctx, member1: Optional[discord.Member]=None, member2: Optional[discord.Member]=None):
    global matches, gameBoards, chances, teamCode
    if ctx.guild.id not in matches:
        matches[ctx.guild.id] = {}
    if ctx.guild.id not in gameBoards:
        gameBoards[ctx.guild.id] = {}
    if ctx.guild.id not in chances:
        chances[ctx.guild.id] = {}
    if ctx.guild.id not in teamCode:
        teamCode[ctx.guild.id] = {}

    if member1 is not None:
        if member2 is None:
            member2 = member1
            member1 = ctx.author
        if member2 != member1:
            # print(list(matches.items()))
            if member1.id not in matches[ctx.guild.id].keys() and member1.id not in matches[ctx.guild.id].values():
                if member2.id not in matches[ctx.guild.id].keys() and member2.id not in matches[ctx.guild.id].values():
                    
                    codeGenerator = random.randint(000000, 999999)
                    while codeGenerator in teamCode[ctx.guild.id].values():
                        codeGenerator = random.randint(000000, 999999)

                    teamCode[ctx.guild.id][member1.id] = codeGenerator
                    teamCode[ctx.guild.id][member2.id] = teamCode[ctx.guild.id][member1.id]

                    if codeGenerator not in gameBoards[ctx.guild.id]:
                        gameBoards[ctx.guild.id][codeGenerator] = {}              

                    await ctx.send(f"**❎ TicTacToe Game 🅾️**")
                    gameBoards[ctx.guild.id][codeGenerator]["boardpiece"] = {"piece1" : "🔳","piece2" : "🔳","piece3" : "🔳","piece4" : "🔳","piece5" : "🔳","piece6" : "🔳","piece7" : "🔳","piece8" : "🔳","piece9" : "🔳"}
                    gameBoards[ctx.guild.id][codeGenerator]["board"] = await ctx.send(f'\n{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece1"]}{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece2"]}{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece3"]}\n{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece4"]}{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece5"]}{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece6"]}\n{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece7"]}{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece8"]}{gameBoards[ctx.guild.id][codeGenerator]["boardpiece"]["piece9"]}')
                    chances[ctx.guild.id][member1.id] = "X"
                    chances[ctx.guild.id][member2.id] = "O"
                    await ctx.send(f"\n Players are {member1.mention} ❎ and {member2.mention} 🅾️\n Send 1 to 9 in the Chat to Use your Turn")

                    matches[ctx.guild.id][member1.id] = member2.id
                    gameBoards[ctx.guild.id][codeGenerator]["blocks"] = {"block1" : False, "block2": False, "block3" : False, "block4": False, "block5" : False,"block6": False, "block7": False, "block8": False, "block9": False}


                    gameBoards[ctx.guild.id][codeGenerator]["chance"] = "X"
                    # print(list(matches.items()))
                    
                else:
                    await ctx.send(f":exclamation: {member2.mention} is Already in a TicTacToe Match in this Server")
            else:
                if member1 == ctx.author:
                    await ctx.send(f":exclamation: {ctx.author.mention} You are Already in a TicTacToe Match in this Server, use `>tttstop` to Stop your Current Match")
                else:
                    await ctx.send(f":exclamation: {member1.mention} is Already in a TicTacToe Match in this Server")
        else:
            if member2 == ctx.author and member1 == ctx.author:
                await ctx.send(f":exclamation: {ctx.author.mention} You Cannot Play With Yourself, There must be Two Players to Play TicTacToe")
            else:
                await ctx.send(f":exclamation: {ctx.author.mention} Single Player Cannot Play with Himself/Herself, There must be Two Players")
    else:
        await ctx.send(f":exclamation: {ctx.author.mention} You are Using The Command Wrong, Use `>help tictactoe` to get help related with the Command")


tictactoehelp = f"tictactoe [First Player] <Second Player>"

@bot.command()
async def tttstop(ctx):
    global matches, gameBoards, chances, teamCode
    try:
        if ctx.author.id in matches[ctx.guild.id].keys() or ctx.author.id in matches[ctx.guild.id].values():
            await ctx.send(f"{ctx.author.mention} Your TicTacToe Game has been Stopped")
            
            if ctx.author.id in matches[ctx.guild.id].keys():
                player1 = ctx.author.id
                player2 = matches[ctx.guild.id][player1]
            elif ctx.author.id in matches[ctx.guild.id].values():
                for id in matches[ctx.guild.id].values():
                    if matches[ctx.guild.id][id] == ctx.author.id:
                        player1 = id
                        player2 = matches[ctx.guild.id][id]
            code = teamCode[ctx.guild.id][ctx.author.id]
            del matches[ctx.guild.id][player1]
            del matches[ctx.guild.id][player2]
            del teamCode[ctx.guild.id][player1]
            del teamCode[ctx.guild.id][player2]
            del gameBoards[ctx.guild.id][code]
        else:
            await ctx.send(f":exclamation: {ctx.author.mention} You are Not in any TicTacToe Match in this Server")
    except Exception as e:
        print(e)
        pass
    

tttstophelp = f"tttstop"

@bot.listen()
async def on_message(message):
    global matches, gameBoards, chances
    try:
        if message.author.id in matches[message.guild.id].keys() or message.author.id in matches[message.guild.id].values():
            userTeam = teamCode[message.guild.id][message.author.id]
            if gameBoards[message.guild.id][userTeam]["chance"] == chances[message.guild.id][message.author.id]:
                if chances[message.guild.id][message.author.id] == "X":
                    if "1" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block1"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block1"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "2" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block2"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block2"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "3" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block3"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block3"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "4" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block4"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block4"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "5" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block5"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block5"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "6" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block6"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block6"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "7" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block7"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block7"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "8" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block8"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block8"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"
                    elif "9" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block9"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] = "❎"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block9"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "O"

                elif chances[message.guild.id][message.author.id] == "O":
                    if "1" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block1"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block1"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "2" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block2"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block2"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "3" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block3"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block3"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "4" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block4"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block4"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "5" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block5"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block5"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "6" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block6"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block6"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "7" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block7"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block7"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "8" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block8"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block8"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"
                    elif "9" in message.content.lower():
                        if gameBoards[message.guild.id][userTeam]["blocks"]["block9"] == False:
                            gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] = "🅾️"
                            await gameBoards[message.guild.id][userTeam]["board"].edit(content=f'\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"]}\n{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"]}{gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"]}')
                            gameBoards[message.guild.id][userTeam]["blocks"]["block9"] = True
                            gameBoards[message.guild.id][userTeam]["chance"] = "X"

            if message.author != bot.user:
                if "1" == message.content.lower() or "2" == message.content.lower() or "3" == message.content.lower() or "4" == message.content.lower() or "5" == message.content.lower() or "6" == message.content.lower() or "7" == message.content.lower() or "8" == message.content.lower() or "9" == message.content.lower():
                    await message.delete()
            ### winner ###
            #
            #
            #
            #
            if gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "❎" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] == "❎":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "X":
                    await message.channel.send(f"<@{player1}> ❎ Won the TicTacToe Match from <@{player2}> 🅾️")
                elif chances[message.guild.id][player2] == "X":
                    await message.channel.send(f"<@{player2}> ❎ Won the TicTacToe Match from <@{player1}> 🅾️")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]


            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] == "🅾️" and gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] == "🅾️":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                if chances[message.guild.id][player1] == "O":
                    await message.channel.send(f"<@{player1}> 🅾️ Won the TicTacToe Match from <@{player2}> ❎")
                elif chances[message.guild.id][player2] == "O":
                    await message.channel.send(f"<@{player2}> 🅾️ Won the TicTacToe Match from <@{player1}> ❎")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            elif gameBoards[message.guild.id][userTeam]["boardpiece"]["piece1"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece2"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece3"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece4"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece5"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece6"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece7"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece8"] != "🔳" and  gameBoards[message.guild.id][userTeam]["boardpiece"]["piece9"] != "🔳":
                if message.author.id in matches[message.guild.id].keys():
                    player1 = message.author.id
                    player2 = matches[message.guild.id][player1]
                elif message.author.id in matches[message.guild.id].values():
                    for id in matches[message.guild.id].values():
                        if matches[message.guild.id][id] == message.author.id:
                            player1 = id
                            player2 = matches[message.guild.id][id]
                await message.channel.send(f"<@{player1}> <@{player2}> The TicTacToe Match is a Tie  ;-;")

                code = teamCode[message.guild.id][message.author.id]
                del matches[message.guild.id][player1]
                del matches[message.guild.id][player2]
                del teamCode[message.guild.id][player1]
                del teamCode[message.guild.id][player2]
                del gameBoards[message.guild.id][code]

            ### winner close ###
        else:
            pass
    except Exception as e:
        print(e)
        pass

@bot.command()
async def poll(ctx, question:Optional[str]=None, option1: Optional[str]=None, option2: Optional[str]=None, option3: Optional[str]=None, option4: Optional[str]=None, option5: Optional[str]=None, option6: Optional[str]=None, option7: Optional[str]=None, option8: Optional[str]=None, option9: Optional[str]=None, option10: Optional[str]=None):
    try:
        if "?" not in question:
            question = question +"?"
        if '"' in ctx.message.content:
            if option1 is not None and option2 is not None:
                if option10 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n 4️⃣ {option4}\n\n 5️⃣ {option5}\n\n 6️⃣ {option6}\n\n 7️⃣ {option7}\n\n 8️⃣ {option8}\n\n 9️⃣ {option9}\n\n 🔟 {option10}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                elif option9 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n 4️⃣ {option4}\n\n 5️⃣ {option5}\n\n 6️⃣ {option6}\n\n 7️⃣ {option7}\n\n 8️⃣ {option8}\n\n 9️⃣ {option9}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                elif option8 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n 4️⃣ {option4}\n\n 5️⃣ {option5}\n\n 6️⃣ {option6}\n\n 7️⃣ {option7}\n\n 8️⃣ {option8}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                elif option7 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n 4️⃣ {option4}\n\n 5️⃣ {option5}\n\n 6️⃣ {option6}\n\n 7️⃣ {option7}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                elif option6 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n 4️⃣ {option4}\n\n 5️⃣ {option5}\n\n 6️⃣ {option6}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                elif option5 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n 4️⃣ {option4}\n\n 5️⃣ {option5}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                elif option4 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n 4️⃣ {option4}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                elif option3 is not None:
                    reactions = ["1️⃣","2️⃣","3️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n 3️⃣ {option3}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")
                else:
                    reactions = ["1️⃣","2️⃣"]
                    pollEmbed = discord.Embed(title=f"{question}  🤔", description=f"1️⃣ {option1}\n\n 2️⃣ {option2}\n\n ", color=embedTheme)
                    pollEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Poll by {ctx.author}")

                pollMsg = await ctx.send(embed=pollEmbed)
                for reaction in reactions:
                    await pollMsg.add_reaction(reaction)      

            else:
                await ctx.send(f":exclamation: {ctx.author.mention} You Must Give Minimum 2 Options!",delete_after=12)
        else:
            await ctx.send(f':exclamation: {ctx.author.mention} The Question/Statement Should be Between Double Quotes, Example - `"<question>"`',delete_after=12)
    except Exception as e:
        print(e)
        await ctx.send(f":exclamation: {ctx.author.mention} You are Doing Mistake in Using the Command, Use `>help poll` to get help for this Command",delete_after=12)

pollhelp = '>poll <question between "f" [options -> (Minimum 2 - Maximum 10) between ""]'

@bot.command()
async def slap(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    # if member is None:
    #     member = bot.user
    if member is not None:
        embed1 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Slapped {member.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Slapped {member.mention} because {ctx.author.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Slapped {member.mention} because {ctx.author.name} went Angry **", color=embedTheme)
        embed4 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Jumped from High Place and Slapped {member.mention} **", color=embedTheme)
    else:
        embed1 = discord.Embed(description=f"** Slapped: {bot.user.mention} Slapped {ctx.author.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"** Slapped: {bot.user.mention} Slapped {ctx.author.mention} because {bot.user.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"** Slapped: {bot.user.mention} Slapped {ctx.author.mention} because {bot.user.name} went Angry **", color=embedTheme)
        embed4 = discord.Embed(description=f"** Slapped: {bot.user.mention} Jumped from High Place and Slapped {ctx.author.mention} **", color=embedTheme)
    allEmbeds = [embed1,embed2,embed3,embed4]
    if reason is None:
        choice = random.choice(allEmbeds)
    else:
        if member is not None:
            arguments = [f"Slapped {member.mention}",f"Jumped from High Place and Slapped {member.mention}"]
        else:
            arguments = [f"Slapped {ctx.author.mention}",f"Jumped from High Place and Slapped {ctx.author.mention}"]
        randomArgu = random.choice(arguments)
        if member is not None:
            choice = discord.Embed(description=f"** Slapped: {ctx.author.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
        else:
            choice = discord.Embed(description=f"** Slapped: {bot.user.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
    await ctx.send(embed=choice)

slaphelp = f"slap [member] [reason]"

@bot.command()
async def kill(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    # if member is None:
    #     member = bot.user
    if member is not None:
        embed1 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} for his Last Birth's Revenge **", color=embedTheme)
        embed3 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} because {ctx.author.name} went Mad **", color=embedTheme)
        embed4 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} by Knife **", color=embedTheme)
        embed5 = discord.Embed(description=f"** Killed: {ctx.author.mention} Shooted {member.mention} by Shotgun **", color=embedTheme)
        embed6 = discord.Embed(description=f"** Killed: {ctx.author.mention} Stabbed Knife to {member.mention} **", color=embedTheme)
    else:
        embed1 = discord.Embed(description=f"** Killed: {bot.user.mention} Killed {ctx.author.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"** Killed: {bot.user.mention} Killed {ctx.author.mention} for his Last Birth's Revenge **", color=embedTheme)
        embed3 = discord.Embed(description=f"** Killed: {bot.user.mention} Killed {ctx.author.mention} because {bot.user.name} went Mad **", color=embedTheme)
        embed4 = discord.Embed(description=f"** Killed: {bot.user.mention} Killed {ctx.author.mention} by Knife **", color=embedTheme)
        embed5 = discord.Embed(description=f"** Killed: {bot.user.mention} Shooted {ctx.author.mention} by Shotgun **", color=embedTheme)
        embed6 = discord.Embed(description=f"** Killed: {bot.user.mention} Stabbed Knife to {ctx.author.mention} **", color=embedTheme)
    allEmbeds = [embed1,embed2,embed3,embed4,embed5,embed6]
    if reason is None:
        choice = random.choice(allEmbeds)
    else:
        if member is not None:
            arguments = [f"Killed {member.mention}",f"Shooted {member.mention} by Shotgun",f"Stabbed Knife to {member.mention}",f"Pushed {member.mention} from High Building"]
        else:
            arguments = [f"Killed {ctx.author.mention}",f"Shooted {ctx.author.mention} by Shotgun",f"Stabbed Knife to {ctx.author.mention}",f"Pushed {ctx.author.mention} from High Building"]
        randomArgu = random.choice(arguments)
        if member is not None:
            choice = discord.Embed(description=f"** Killed: {ctx.author.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
        else:
            choice = discord.Embed(description=f"** Killed: {bot.user.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
    await ctx.send(embed=choice)

killhelp = f"kill [member] [reason]"

@bot.command()
async def punch(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    # if member is None:
    #     member = bot.user
    if member is not None:
        embed1 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} because {ctx.author.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} on his Nose **", color=embedTheme)
        embed4 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} in Voilence **", color=embedTheme)
    else:
        embed1 = discord.Embed(description=f"** Punched: {bot.user.mention} Punched {ctx.author.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"** Punched: {bot.user.mention} Punched {ctx.author.mention} because {bot.user.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"** Punched: {bot.user.mention} Punched {ctx.author.mention} on his Nose **", color=embedTheme)
        embed4 = discord.Embed(description=f"** Punched: {bot.user.mention} Punched {ctx.author.mention} in Voilence **", color=embedTheme)

    allEmbeds = [embed1,embed2,embed3,embed4]
    if reason is None:
        choice = random.choice(allEmbeds)
    else:
        if member is not None:
            arguments = [f"Punched {member.mention}",f"Punched on {member.mention}'s Nose",f"Punched {member.mention} in Voilence"]
        else:
            arguments = [f"Punched {ctx.author.mention}",f"Punched on {ctx.author.mention}'s Nose",f"Punched {ctx.author.mention} in Voilence"]
        randomArgu = random.choice(arguments)
        if member is not None:
            choice = discord.Embed(description=f"** Punched: {ctx.author.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
        else:
            choice = discord.Embed(description=f"** Punched: {bot.user.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
    await ctx.send(embed=choice)  

punchhelp = f"punch [member] [reason]"

@bot.command()
async def wanted(ctx, member: Optional[discord.Member]=None):
    if member is None:
        member = ctx.author
    wantedimg = Image.open("wanted.jpg")
    pfp = member.avatar_url_as(size = 128)
    data = BytesIO(await pfp.read())
    loadPfp = Image.open(data)

    loadPfp = loadPfp.resize((177,177))

    wantedimg.paste(loadPfp, (120,212))
    wantedimg.save("profile.jpg")

    await ctx.send(file = discord.File("profile.jpg"))


wantedhelp = f"wanted [member]"

afkdata = {}
username = {}
reasontopic = {}

@bot.command()
async def afk(ctx, *, reason: Optional[str]=None):
    global afkdata, username, reasontopic
    try:
        if ctx.guild.id not in afkdata:
            afkdata[ctx.guild.id] = []

        # print(afkdata)
        if ctx.author not in afkdata[ctx.guild.id]:
            username[ctx.author.id] = ctx.author.nick
            if reason is None:
                reason = f"Afk"
            reasontopic[ctx.author.id] = reason
            # embed = discord.Embed(description=f"Afk Set : {reason}", color=embedTheme)
            # await ctx.send(embed=embed)
            await ctx.send(f"{ctx.author.mention} Afk Set : {reason}")
            try:
                await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")
            except:
                pass

            afkdata[ctx.guild.id].append(ctx.author.id)
            # print(list(afkdata[ctx.guild.id].keys()))
            # print(afkdata)
        else:
            await ctx.send(f"{ctx.author.mention} You Afk has been Removed, User `>afk` Again to Set Your Afk")
    except Exception as e:
        print(e)
        pass

afkhelp = f"afk [reason]"

@bot.listen()
async def on_message(message):
    global afkdata, reasontopic
    # print(afkdata)
    # print(reasontopic)
    # if not message.author.bot:
    if message.guild.id not in afkdata:
            afkdata[message.guild.id] = []
    users = afkdata[message.guild.id]
    print(users)
    if len(users) > 0:
        # print(users)
        for user in users:
            # print(user)
            username = await bot.fetch_user(user)
            print(username)
            if f"<@{user}>" in message.content:
                print(1)
                if user in afkdata[message.guild.id]:
                    print(2)
                    await message.channel.send(f"Afk: {message.author.mention} He is Currently Afk | Reason: {reasontopic[user]}")
            else:
                # print("He is not afk")
                pass

@bot.listen()
async def on_message(message):   
    global afkdata, username, reasontopic
    # print(afkdata)
    try:
        if message.author.id in afkdata[message.guild.id]:
            afkdata[message.guild.id].remove(message.author.id)
            await message.channel.send(f"Afk Removed: {message.author.mention} You are no More Afk Now!")
            try:
                await message.author.edit(nick=username[message.author.id])
            except:
                pass
            del username[message.author.id]
            del reasontopic[message.author.id]
    except Exception as e:
        print(e)
        pass

@bot.command()
async def support(ctx):
    try:
        embed = discord.Embed(title="Support", description="To get Support, Join our Official Server Where you are Free to Report Bugs, Get Help, Give Suggestions, Ask Problems and Doubts, tell about Crashes and Many More involving Fun With Our Team \:)\n\n[Get Support Now](https://discord.gg/H3688EEpWr)", color=embedTheme)
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        pass

supporthelp = f"support"

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

rulehelp = f"rule <rule no.>"
   
@bot.command()
async def rules(ctx):
    server_prefix = await bot.pg_con.fetchrow("SELECT prefix FROM prefixes WHERE guild_id  = $1", ctx.guild.id)
    embed = discord.Embed(title="Server Rules", description="These are some Rules of this Server", color= embedTheme)
    embed.add_field(name="1. No Promotion",value=f"  type {ctx.prefix}rule 1 for more info",inline= False)
    embed.add_field(name="2. No Abuses",value=f"  type {ctx.prefix}rule 2 for more info",inline= False)
    embed.add_field(name="3. No Spamming",value=f"  type {ctx.prefix}rule 3 for more info",inline= False)
    embed.add_field(name="4. No Toxicity",value=f"  type {ctx.prefix}rule 4 for more info\n\n",inline= False)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

ruleshelp = f"rules"

@bot.command()
async def avatar(ctx, owner: Optional[discord.Member]=None):
    if owner is None:
        owner = ctx.author
    embed = discord.Embed(title="Avatar",color=embedTheme)
    embed.set_author(icon_url=owner.avatar_url,name=owner)
    embed.set_image(url=owner.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

avatarhelp = f"avatar [user]"

@bot.command()
async def vote(ctx):
    symbol = " ♦ "
    embed = discord.Embed(title="Vote For Tornax\t\t", color=embedTheme)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Click on Below Links", value=f"{symbol}[Top.gg](https://top.gg/bot/832897602768076816/vote)\n{symbol}[Discord Bot List](https://discordbotlist.com/bots/tornax/upvote)\n", inline=False)
    embed.add_field(name="Rewards", value="Join Our Official Server Now For Op Rewards Daily !!", inline=False)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

votehelp = f"vote"

@bot.command()
async def info(ctx):
    Listedgreetings = ["Hello!","Hi!","Hey!","Heya!"]
    RandomGreetings = random.choice(Listedgreetings)
    embed = discord.Embed(title="My Information",description=f"{RandomGreetings} I am Tornax a Multi-Talented Discord Bot, Designed, Created and Configured by MrinalSparks\n\nCurrently I Am In : {len(list(bot.guilds))} Servers", color=embedTheme)
    await ctx.send(embed=embed)

infohelp = f"info"

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="About Tornax",description="Tornax is a Multi-Talented and Friendly Bot, Use Tornax for moderation, server managements, streams and giveaways now!", color=embedTheme)
    await ctx.send(embed=embed)

abouthelp = f"about"

helphelp = f"help [anycommand]"

allcommandshelp = f"allcommands"

@bot.command()
async def help(ctx, anycommand: Optional[str]=None):
    server_prefix = await bot.pg_con.fetchrow("SELECT prefix FROM prefixes WHERE guild_id  = $1", ctx.guild.id)

    print(bot.all_commands.keys())
    totalCommands = len(bot.all_commands.keys())

    servers = list(bot.guilds)
    print("Currently on " + str(len(bot.guilds)) + " Servers:")
    for x in range(len(servers)):
        print('  ' + servers[x-1].name)

    print(totalCommands)
    if anycommand is None:
        randomGreet = random.choice(["Hi","Hey","Hello"])
        myEmbed = discord.Embed(color = embedTheme)
        myEmbed.add_field(name=f"{randomGreet} There! I'm Tornax",value="A Multi-Talented and Friendly Bot, Use Tornax for Moderation, Server Managements, Streaming and Giveaways now!\n \n \t-> [Invite Tornax to your Server Now!](https://discord.com/api/oauth2/authorize?client_id=832897602768076816&permissions=536870911991&scope=bot)")
        myEmbed.add_field(name=f"Commands — {int(totalCommands)-2}",value="----------------------\n",inline=False)
        myEmbed.add_field(name="Miscellaneous",value=" tell, poll, ping, afk, thought, vote, avatar, react, rule, rules, solve, time, timerstart, timerstop ", inline=False)
        myEmbed.add_field(name="Management",value=" addrole, removerole, clean, gstart, allcommands, gstatus, gstop, gparticipate, gquit, setprefix, info, invite, about, support, join, leave, leaveserver, lock, slowmode, resetnick, setnick, unlock ", inline=False)
        myEmbed.add_field(name="Moderation",value=" kick, mute, warn, unmute, ban, unban ", inline=False)
        myEmbed.add_field(name="Fun",value=" slap, kill, punch, wanted, tictactoe, tttstop, guess, mcserver, wikipedia, google \n----------------------\n", inline=False)
        myEmbed.add_field(name="\n\n**Official Server**",value=f"----------------------\nJoin Our Official Server for More Commands and Help \n\n \t-> [Join Now](https://discord.gg/H3688EEpWr)\n----------------------\n\n > Server's Current Prefix is :   `{ctx.prefix}`\n > Command Usage Example :   `{ctx.prefix}info`\n\n----------------------", inline=False)
        myEmbed.add_field(name="Readme", value=f"`{ctx.prefix}help` Shows this Message, use `{ctx.prefix}help [command]` to get more information about that Command\n\n")
        myEmbed.set_footer(icon_url=bot.user.avatar_url,text=f"Made by {Creater}")
        await ctx.send(embed=myEmbed)
    else:
        content = ""

        if anycommand == "tell": content=tellhelp
        elif anycommand == "ping": content=pinghelp
        elif anycommand == "invite": content=invitehelp
        elif anycommand == "thought": content=thoughthelp
        elif anycommand == "avatar": content=avatarhelp
        elif anycommand == "afk": content=afkhelp
        elif anycommand == "react": content=reacthelp
        elif anycommand == "rule": content=rulehelp
        elif anycommand == "rules": content=ruleshelp
        elif anycommand == "solve": content=solvehelp
        elif anycommand == "time": content=timehelp
        elif anycommand == "timerstart": content=timerstarthelp
        elif anycommand == "timerstop": content=timerstophelp
        elif anycommand == "addrole": content=addrolehelp
        elif anycommand == "removerole": content=removerolehelp
        elif anycommand == "clean": content=cleanhelp
        elif anycommand == "gstart": content=gstarthelp
        elif anycommand == "gstatus": content=gstatushelp
        elif anycommand == "gstop": content=gstophelp
        elif anycommand == "gparticipate": content=gparticipatehelp
        elif anycommand == "gquit": content=gquithelp
        elif anycommand == "poll": content=pollhelp
        elif anycommand == "info": content=infohelp
        elif anycommand == "setprefix": content=setprefixhelp
        elif anycommand == "about": content=abouthelp
        elif anycommand == "vote": content=votehelp
        elif anycommand == "support": content=supporthelp
        elif anycommand == "wikipedia": content=wikipediahelp
        elif anycommand == "google": content=googlehelp
        elif anycommand == "join": content=joinhelp
        elif anycommand == "leave": content=leavehelp
        elif anycommand == "leaveserver": content=leaveserverhelp
        elif anycommand == "lock": content=lockhelp
        elif anycommand == "unlock": content=unlockhelp
        elif anycommand == "slowmode": content=slowmodehelp
        elif anycommand == "setnick": content=setnickhelp
        elif anycommand == "resetnick": content=resetnickhelp
        elif anycommand == "kick": content=kickhelp
        elif anycommand == "mute": content=mutehelp
        elif anycommand == "warn": content=warnhelp
        elif anycommand == "unmute": content=unmutehelp
        elif anycommand == "ban": content=banhelp
        elif anycommand == "unban": content=unbanhelp
        elif anycommand == "slap": content=slaphelp
        elif anycommand == "kill": content=killhelp
        elif anycommand == "punch": content=punchhelp
        elif anycommand == "wanted": content=wantedhelp
        elif anycommand == "tictactoe": content=tictactoehelp
        elif anycommand == "tttstop": content=tttstophelp
        elif anycommand == "guess": content=guesshelp
        elif anycommand == "mcserver": content=mcserverhelp
        elif anycommand == "allcommands": content=allcommandshelp
        elif anycommand == "help": content=helphelp
        commandEmbed = discord.Embed(description=f"{ctx.prefix}{content}",color=embedTheme)
        await ctx.send(embed=commandEmbed)

activecmd = {}
cmdcode = {}

@bot.command()
async def allcommands(ctx):
    global activecmd, cmdcode
    if ctx.guild.id not in activecmd:
        activecmd[ctx.guild.id] = {}
    if ctx.guild.id not in cmdcode:
        cmdcode[ctx.guild.id] = {}

    if ctx.author.id in cmdcode[ctx.guild.id]:
        code = cmdcode[ctx.guild.id][ctx.author.id]
        await activecmd[ctx.guild.id][code]["message"].clear_reactions()

    genCode = random.randint(000000, 999999)
    while genCode in activecmd[ctx.guild.id].keys():
        genCode = random.randint(000000, 999999)
    cmdcode[ctx.guild.id][ctx.author.id] = genCode
    activecmd[ctx.guild.id][genCode] = {}
    activecmd[ctx.guild.id][genCode]["page"] = 1

    sign = "→"

    toolsList = {f"{ctx.prefix}tell":"Send Your Message From Tornax for Announcements and Fun",f"{ctx.prefix}poll":"Easily Host Reaction Based Polls",f"{ctx.prefix}ping":"Get the Current Latency in ms value",f"{ctx.prefix}afk":"Let Others Know Your Status and What are You Doing Currently",f"{ctx.prefix}thought":"Show your Current Thinking in a Different & Higlighted Way",f"{ctx.prefix}avatar":"See Someone's Profile Picture/Avatar in Large Size",f"{ctx.prefix}react":"Let Tornax React on a Message for You",f"{ctx.prefix}solve":"Use Tornax for Simple to Difficult Calculations",f"{ctx.prefix}timerstart":"Let Tornax Start Countdown for You",f"{ctx.prefix}timerstop":"Stop The Countdown in Between Started by Tornax"}
    toolscmd = []
    for cmd in list(toolsList.keys()):
        toolscmd.append(f"• {cmd} {sign}  {toolsList[cmd]}.")
    toolscmd = " \n ".join(toolscmd)

    toolsEmbed = discord.Embed(title="Tools Commands", description=f"{toolscmd} \n\n 1/8", color=embedTheme)

    managementList = {f"{ctx.prefix}addrole":"Give/Add Any Role to Anyone",f"{ctx.prefix}removerole":"Take/Remove Any Role From Anyone",f"{ctx.prefix}clean":"Clean/Delete So Many Messages Quickly by Just Specifing the Quanitity",f"{ctx.prefix}setprefix":"Change Prefix of Tornax According to your Choice",f"{ctx.prefix}join":"Let Tornax Join a Voice Channel With You",f"{ctx.prefix}leave":"Let Tornax Leave a Voice Channel",f"{ctx.prefix}leaveserver":"Tell Tornax to Leave Your Server \:(",f"{ctx.prefix}lock":"Lock any Channel of Your Server to Disallow Members to Send Messages in it",f"{ctx.prefix}unlock":"Unlock a Locked Channel of Your Server",f"{ctx.prefix}slowmode":"Set Slowmode for a Channel of Your Server",f"{ctx.prefix}setnick":"Set or Change Nick of YourSelf or any Member",f"{ctx.prefix}resetnick":"Reset/Remove Your or SomeBodies Nick"}
    managementcmd = []
    for cmd in list(managementList.keys()):
        managementcmd.append(f"• {cmd} {sign}  {managementList[cmd]}.")
    managementcmd = " \n ".join(managementcmd)
    managementEmbed = discord.Embed(title="Management Commands", description=f"{managementcmd} \n\n 2/8", color=embedTheme)
    
    giveawayList = {f"{ctx.prefix}gstart":"Start and Host a New Giveaway",f"{ctx.prefix}gparticipate":"Participate in Currently Active Giveaway",f"{ctx.prefix}gquit":"Quit the Giveaway of a Server in Between",f"{ctx.prefix}gstatus":"Get the Active Giveaway Status of Your Server",f"{ctx.prefix}gstop":"Stop a Giveaway in Between"}
    giveawaycmd = []
    for cmd in list(giveawayList.keys()):
        giveawaycmd.append(f"• {cmd} {sign}  {giveawayList[cmd]}.")
    giveawaycmd = " \n ".join(giveawaycmd)
    giveawayEmbed = discord.Embed(title="Giveaways Commands", description=f"{giveawaycmd} \n\n 3/8", color=embedTheme)

    moderationList = {f"{ctx.prefix}kick":"Kick Anyone From Your Server",f"{ctx.prefix}mute":"Mute a Member of Your Server",f"{ctx.prefix}unmute":"Unmute a Muted Member in Your Server",f"{ctx.prefix}warn":"Warn a Member of Your Server With/Without a Reason",f"{ctx.prefix}ban":"Ban a Member from your Server Permanently or Temporary",f"{ctx.prefix}unban":"Unban a Banned Member in Your Server"}
    moderationcmd = []
    for cmd in list(moderationList.keys()):
        moderationcmd.append(f"• {cmd} {sign}  {moderationList[cmd]}.")
    moderationcmd = " \n ".join(moderationcmd)
    moderationEmbed = discord.Embed(title="Moderation Commands", description=f"{moderationcmd} \n\n 4/8", color=embedTheme)

    funList = {f"{ctx.prefix}slap":"Slap Somebody with a Highlighted Text",f"{ctx.prefix}kill":"Kill Somebody with a Highlighted Text",f"{ctx.prefix}punch":"Punch Somebody with a Highlighted Text",f"{ctx.prefix}wanted":"Make Somebody a Wanted Person with Cash Prize"}
    funcmd = []
    for cmd in list(funList.keys()):
        funcmd.append(f"• {cmd} {sign}  {funList[cmd]}.")
    funcmd = " \n ".join(funcmd)
    funEmbed = discord.Embed(title="Fun Commands", description=f"{funcmd} \n\n 5/8", color=embedTheme)

    minigamesList = {f"{ctx.prefix}tictactoe":"Challenge Your Friends for a Tictactoe Match",f"{ctx.prefix}tttstop":"Stop a Tictactoe Game in Between",f"{ctx.prefix}guess":"Start a Guess the Number Challenge with Your Server Members"}
    minigamescmd = []
    for cmd in list(minigamesList.keys()):
        minigamescmd.append(f"• {cmd} {sign}  {minigamesList[cmd]}.")
    minigamescmd = " \n ".join(minigamescmd)
    minigamesEmbed = discord.Embed(title="Mini-Games Commands", description=f"{minigamescmd} \n\n 6/8", color=embedTheme)

    infoList = {f"{ctx.prefix}rule":"Get a Rule of a Server in Detail",f"{ctx.prefix}rules":"Get all Rules of a Server in a Listed and Proper Manner",f"{ctx.prefix}mcserver":"Get Status and Details of a Minecraft Java Server",f"{ctx.prefix}wikipedia":"Get a Biography or Informations in Details of a Particular Topic with Wikipedia",f"{ctx.prefix}google":"Get all Links Related With your Topic Quickly and in a Listed Manner"}
    infocmd = []
    for cmd in list(infoList.keys()):
        infocmd.append(f"• {cmd} {sign}  {infoList[cmd]}.")
    infocmd = " \n ".join(infocmd)
    infoEmbed = discord.Embed(title="Information Commands", description=f"{infocmd} \n\n 7/8", color=embedTheme)

    generalList = {f"{ctx.prefix}info":"Get Information of Tornax in a brief way",f"{ctx.prefix}support":"Get Advantages, Details and Link of Our Official Server",f"{ctx.prefix}vote":"Get Tornax Voting Link with Rewards Information",f"{ctx.prefix}time":"Get the Current Time of Tornax",f"{ctx.prefix}invite":"Get a Link to Invite Tornax",f"{ctx.prefix}about":"Get Details and Information about Tornax with its Specialities"}
    generalcmd = []
    for cmd in list(generalList.keys()):
        generalcmd.append(f"• {cmd} {sign}  {generalList[cmd]}.")
    generalcmd = " \n ".join(generalcmd)
    generalEmbed = discord.Embed(title="General Commands", description=f"{generalcmd} \n\n 8/8", color=embedTheme)

    print(len(toolsList.keys()) + len(managementList.keys()) + len(giveawayList.keys()) + len(moderationList.keys()) + len(funList.keys()) + len(minigamesList.keys()) + len(infoList.keys()) + len(generalList.keys()))

    activecmd[ctx.guild.id][genCode]["message"] = await ctx.send(embed=toolsEmbed)
    controlbuttons = ["🔢","⏮️","◀️","▶️","⏭️","⏹️"]
    for btns in controlbuttons:
        await activecmd[ctx.guild.id][genCode]["message"].add_reaction(btns)
    
    activecmd[ctx.guild.id][genCode]["Embeds"] = [toolsEmbed,managementEmbed,giveawayEmbed,moderationEmbed,funEmbed,minigamesEmbed,infoEmbed,generalEmbed]

    await asyncio.sleep(300)
    if ctx.author.id in cmdcode[ctx.guild.id]:
        await activecmd[ctx.guild.id][genCode]["message"].clear_reactions()
        del activecmd[ctx.guild.id][genCode]
        del cmdcode[ctx.guild.id][ctx.author.id]

@bot.listen()
async def on_reaction_add(reaction, user):
    global cmdcode, activecmd
    try:
        if user.id != bot.user.id:
            if user.id in cmdcode[reaction.message.guild.id]:
                print(1)
                if user.id in cmdcode[reaction.message.guild.id]:
                    code = cmdcode[reaction.message.guild.id][user.id]
                    print(activecmd[reaction.message.guild.id][code]["page"])
                    messge = activecmd[reaction.message.guild.id][code]["message"]
                    if reaction.message.id == messge.id:
                        print(2)
                        if reaction.emoji == "🔢":
                            await messge.remove_reaction("🔢", user)
                            asking = await reaction.message.channel.send(f"In Which Page You Want to Jump?")
                            replymsg = await bot.wait_for(event="message",timeout=60)
                            if 0 < int(replymsg.content) < 9:
                                await asking.delete()
                                await replymsg.delete()
                                activecmd[reaction.message.guild.id][code]["page"] = replymsg.content
                            else:
                                await replymsg.reply(f":exclamation: That Page doesn't Exist")

                        elif reaction.emoji == "⏮️":
                            await messge.remove_reaction("⏮️", user)
                            activecmd[reaction.message.guild.id][code]["page"] = 1

                        elif reaction.emoji == "◀️":
                            await messge.remove_reaction("◀️", user)
                            activecmd[reaction.message.guild.id][code]["page"] -= 1
                            if activecmd[reaction.message.guild.id][code]["page"] < 1:
                                activecmd[reaction.message.guild.id][code]["page"] = 8

                        elif reaction.emoji == "▶️":
                            await messge.remove_reaction("▶️", user)
                            print(3)
                            activecmd[reaction.message.guild.id][code]["page"] += 1
                            if activecmd[reaction.message.guild.id][code]["page"] > 8:
                                activecmd[reaction.message.guild.id][code]["page"] = 1
                        
                        elif reaction.emoji == "⏭️":
                            await messge.remove_reaction("⏭️", user)
                            activecmd[reaction.message.guild.id][code]["page"] = 8
                        
                        elif reaction.emoji == "⏹️":
                            await messge.remove_reaction("⏹️", user)
                            await activecmd[reaction.message.guild.id][code]["message"].clear_reactions()
                            del activecmd[reaction.message.guild.id][code]
                            del cmdcode[reaction.message.guild.id][user.id]

                        if activecmd[reaction.message.guild.id][code]["page"] == 1:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][0])
                        elif activecmd[reaction.message.guild.id][code]["page"] == 2:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][1])
                        elif activecmd[reaction.message.guild.id][code]["page"] == 3:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][2])
                        elif activecmd[reaction.message.guild.id][code]["page"] == 4:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][3])
                        elif activecmd[reaction.message.guild.id][code]["page"] == 5:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][4])
                        elif activecmd[reaction.message.guild.id][code]["page"] == 6:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][5])
                        elif activecmd[reaction.message.guild.id][code]["page"] == 7:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][6])
                        elif activecmd[reaction.message.guild.id][code]["page"] == 8:
                            await activecmd[reaction.message.guild.id][code]["message"].edit(embed=activecmd[reaction.message.guild.id][code]["Embeds"][7])
            else:
                await reaction.remove(user)
    except Exception as e:
        print(e)
        pass
                
count = {}

@bot.listen()
async def on_message(message):
    global count
    if not message.author.bot:
        if message.guild.id not in count:
            count[message.guild.id]  = {}
        if message.author.id not in count[message.guild.id]:
            count[message.guild.id][message.author.id] = {}
        if "counting" not in count[message.guild.id][message.author.id]:
            count[message.guild.id][message.author.id]["counting"] = False
        if "strikes" not in count[message.guild.id][message.author.id]:
            count[message.guild.id][message.author.id]["strikes"] = 0
        if "warnings" not in count[message.guild.id][message.author.id]:
            count[message.guild.id][message.author.id]["warnings"] = 0

        
        if count[message.guild.id][message.author.id]["counting"] == False:
            count[message.guild.id][message.author.id]["counting"] = True        
        await asyncio.sleep(4)
        count[message.guild.id][message.author.id]["counting"] = False
        count[message.guild.id][message.author.id]["strikes"] = 0
        # print(count[message.guild.id][message.author.id]["counting"])
        await asyncio.sleep(2600)
        count[message.guild.id][message.author.id]["warnings"] = 0

@bot.listen()
async def on_message(message):
    global count
    if message.guild.id not in count:
        count[message.guild.id]  = {}
    if message.author.id not in count[message.guild.id]:
        count[message.guild.id][message.author.id] = {}
    if "counting" not in count[message.guild.id][message.author.id]:
        count[message.guild.id][message.author.id]["counting"] = False
    if "strikes" not in count[message.guild.id][message.author.id]:
        count[message.guild.id][message.author.id]["strikes"] = 0
    if "warnings" not in count[message.guild.id][message.author.id]:
        count[message.guild.id][message.author.id]["warnings"] = 0

    if message.content is not None:
        if not message.author.bot:
            # print(f'Count:{count[message.guild.id][message.author.id]["counting"]}",f"Strikes:{count[message.guild.id][message.author.id]["strikes"]}')
            
            if count[message.guild.id][message.author.id]["counting"] == True:
                count[message.guild.id][message.author.id]["strikes"] += 1
            if count[message.guild.id][message.author.id]["strikes"] > 3:
                await message.channel.send(f":exclamation: {message.author.mention} You are Sending Message So Quickly, Slowdown your Speed")
                count[message.guild.id][message.author.id]["warnings"] += 1
                if count[message.guild.id][message.author.id]["warnings"] >= 3:
                    try:
                        mutedRole = discord.utils.get(message.guild.roles, name="Muted")
                        if not mutedRole:
                            mutedRole = await message.guild.create_role(name="Muted")

                            for channel in message.guild.channels:
                                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                        await message.author.add_roles(mutedRole)
                        embed = discord.Embed(description = f"** {message.author.mention} has been Muted by {bot.user.mention} for `15` Seconds \n\t With the Reason of :\t Spamming**",color=embedTheme)
                        await message.channel.send(embed=embed)
                        count[message.guild.id][message.author.id]["warnings"] = 0
                        await asyncio.sleep(15)
                        await message.author.remove_roles(mutedRole)
                    except:
                        count[message.guild.id][message.author.id]["warnings"] = 0
                        pass

                count[message.guild.id][message.author.id]["strikes"] = 0    

@bot.listen()
async def on_message(message):
    if message.content.lower().startswith(f"botservers"):
        servers = list(bot.guilds)
        print(servers)

restricted_words = ["harami","wtf","fuck","fuk","baap ","stfu"]

@bot.listen()
async def on_message(message):
    if not message.author.bot:
        for word in restricted_words:
            if word in message.content.lower():
                await message.delete()
                await message.channel.send(f":exclamation: The Word you are Using is Not Allowed in this Server {message.author.mention}",delete_after=8)
                
bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN)