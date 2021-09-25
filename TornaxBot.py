import warnings
import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import random
from typing import Optional
import json

from discord.ext.commands import has_permissions,has_role,MissingPermissions,MissingRole,CommandNotFound,CommandInvokeError
from discord.member import Member

bot = commands.Bot(command_prefix = ">",case_insensitive=True ,help_command=None)

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
            embed = discord.Embed(description = f"** {member.mention} has been Banned Successfully by {ctx.author.mention} for `{days}` Days **" if reason is None else f"** {member.mention} has been Banned Successfully by {ctx.author.mention} for `{days}` Days \n\t With the Reason of :\t{reason}**",color=embedTheme)
            dmuser = discord.Embed(description = f"** You are Banned by an Admin from {ctx.guild.name} for `{days}` Days **" if reason is None else f"** You are Banned by an Admin from {ctx.guild.name} for `{days}` Days \n\t With the Reason of :\t{reason}**",color=embedTheme)
            await ctx.send(embed=embed)
            await member.send(embed=dmuser)
            await member.ban(reason=reason)
            await asyncio.sleep(wait)
            await ctx.guild.unban(memberId)
        else:
            embed = discord.Embed(description = f"** {member.mention} has been Banned Successfully by {ctx.author.mention} **" if reason is None else f"** {member.mention} has been Banned Successfully by {ctx.author.mention} \n\t With the Reason of :\t{reason}**",color=embedTheme)
            dmuser = discord.Embed(description = f"** You are Banned by an Admin from {ctx.guild.name} **" if reason is None else f"** You are Banned by an Admin from {ctx.guild.name} \n\t With the Reason of :\t{reason}**",color=embedTheme)
            await ctx.send(embed=embed)
            await member.send(embed=dmuser)
            await member.ban(reason=reason)
    except Exception as e:
        print(e)
        await ctx.reply(f":exclamation: You don't have Permissions to do that!")

banhelp = ">ban <member> [days] [reason]"

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

unbanhelp = ">unban <member id>"

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
                await member.add_roles(mutedRole)
                await ctx.send(embed=embed,delete_after=15)
                await member.send(dmAlert)
                await asyncio.sleep(wait)
                await member.remove_roles(mutedRole)
            else:
                embed = discord.Embed(description=f"** {member.mention} has been Muted Successfully by {ctx.author.mention}**" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention}\n\t With the Reason of :\t{reason}**",color=embedTheme)
                await member.add_roles(mutedRole)
                await ctx.send(embed=embed,delete_after=15)
                await member.send(f"You are Muted in the Server by an Admin"if reason is None else f"You are Muted in the Server by an Admin\n\t With the Reason of {reason}")
        except Exception:
            pass
    except MissingPermissions:
        await ctx.reply(f":exclamation: You don't have Permissions to do that!")

mutehelp = ">mute <member> [duration] [unit = s,m,h] [reason]"

@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member:discord.Member, reason: Optional[str]=None):
    mutedRole = discord.utils.get(ctx.message.guild.roles, name="Muted")
    if mutedRole in member.roles:
        embed = discord.Embed(description=f"** {member.mention} has been Unmuted Successfully by {ctx.author.mention}**" if reason is None else f"** {member.mention} has been Unmuted Successfully by {ctx.author.mention}\n\t With the Reason of :\t{reason}**",color=embedTheme)
        await member.remove_roles(mutedRole)
        await ctx.send(embed=embed,delete_after=15)
    else:
        embed = discord.Embed(description=f"** :exclamation: {member.mention} is Not Muted in this Server **",color=embedTheme)
        await ctx.send(embed=embed,delete_after=15)

unmutehelp = ">unmute <member> [reason]"

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member:discord.Member, *, reason=None):
    if member is not None:
        await ctx.send(f"Warned: {member.mention} has been Warned by {ctx.author.mention}" if reason is None else f"Warned: {member.mention} has been Warned by {ctx.author.mention} \n\t With the Reason of :\t{reason}")
        await member.send(f"You are Warned by an Admin in {ctx.guild.name}"if reason is None else f"You are Warned by an Admin in {ctx.guild.name} \n\t With the Reason of :\t{reason}")
    else:
        await ctx.send(f"You must Specify the User whom you want to Warn")

warnhelp = ">warn <member> [reason]"

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
            await member.kick(reason=reason)
            await ctx.send(f"Kicked: {member.mention} has been Kicked from the Server by {ctx.author.mention}" if reason is None else f"Kicked: {member.mention} has been Kicked from the Server by {ctx.author.mention} \n\t With the Reason of :\t{reason}")
            await member.send(f"You are Kicked by an Admin from {ctx.guild.name}"if reason is None else f"You are Kicked by an Admin from {ctx.guild.name} \n\t With the Reason of :\t{reason}")
    else:
        await ctx.send(f"You must Specify the User whom you want to Kick from the Server")

kickhelp = ">kick <member> [reason]"

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

leaveserverhelp = ">leaveserver"

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

setnickhelp = ">setnick [member] <newname>"

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

resetnickhelp = ">resetnick [member]"

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

cleanhelp = ">clean <limit>"

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

lockhelp = ">lock [channel]"

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

unlockhelp = ">unlock [channel]"

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

slowmodehelp = ">slowmode <seconds>"

@bot.command()
async def thought(ctx, *, word):
    if " " in word:
        word = discord.Embed(description=f"You cannot use More than one Word",color=embedTheme)
        await ctx.send(embed=word,delete_after=8)
    else:
        embed = discord.Embed(title=f"\t{word.upper()}", color=embedTheme)
        await ctx.send(embed=embed)

thoughthelp = ">thought <word>"

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
    @commands.has_role("Giveaway Handler")
    async def gstart(ctx, Channel:discord.TextChannel, prize:str, endtime:int, unit:str):
        global GiveawayActive, GiveawayChannel, StartAnnounce, MembersList, ParticipantsMsg
        try:
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
        except:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}, use `>help gstop` for more help')

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
    @commands.has_role("Giveaway Handler")
    async def gstatus(ctx):
        try:
            if ctx.guild.id not in GiveawayActive:
                GiveawayActive[ctx.guild.id] = False
            if GiveawayActive[ctx.guild.id]:
                await ctx.send(f"A Giveaway is Currently Active in this Server \n Number of Participants :- {Participants[ctx.guild.id]}\n Giveaway Channel :- {GiveawayChannel[ctx.guild.id]}")
            else:
                await ctx.send(":exclamation: There is No Giveaway Active in this Server")
        except:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}, use `>help gstop` for more help')

    @bot.command()
    @commands.has_role("Giveaway Handler")
    async def gstop(ctx):
        global GiveawayActive, Participants, GiveawayChannel, MembersList
        try:
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
        except :
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}, use `>help gstop` for more help')

gstarthelp = ">gstart <channel> <prize> <endtime> <unit , for ex:- s,m,h>"
gstophelp = ">gstop"
gparticipatehelp = ">gparticipate"
gquithelp = ">gquit"
gstatushelp = ">gstatus"

@bot.command()
async def react(ctx, chat:Optional[discord.Message], emoji):
    message = chat
    await message.add_reaction(emoji)

reacthelp = ">react <message id> <emoji>"

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

joinhelp = ">join"

@bot.command()
async def leave(ctx):
    try:
        try:
            await ctx.voice_client.disconnect()
        except:
            await ctx.send(f":exclamation: {ctx.author.mention} Tornax is Not Connected to any Voice Channel!")
    except CommandInvokeError:
        await ctx.send(f":exclamation: {ctx.author.mention} You must be in a Voice Channel to do that!")

leavehelp = ">leave"

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

addrolehelp = ">addrole [member] <role>"

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

removerolehelp = ">removerole [member] <role>"

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
        embed = discord.Embed(title="Command : >solve", description=f"Usage : >solve [Number1] [Operation: +,-,*,/] [Number2]",color=embedTheme)
        await ctx.send(embed=embed)

solvehelp = ">solve <number1> <operation = +,-,×,÷> <number2>"

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

timerstarthelp = ">timerstart <seconds> [reason]"

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

timerstophelp = ">timerstop"

@bot.command()
async def ping(ctx, toping:Optional[discord.Member]=None):
    await ctx.message.delete()
    await ctx.send(toping.mention if toping is not None else ctx.author.mention)

pinghelp = ">ping [whom to ping]"

@bot.command()
@commands.bot_has_permissions(send_messages=True)
async def time(ctx):
    currenttime = datetime.now()
    await ctx.send(f"Current Time is {currenttime}")

timehelp = ">time"

@bot.command()
async def tell(ctx, channel: Optional[discord.TextChannel]=None, *, msg):
    if channel is None:
        channel = ctx.channel
    await channel.send(msg)

tellhelp = ">tell [channel] <message>"

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
                await ctx.send(f":exclamation: {ctx.author.mention} You Cannot Play With Yourself, There must be Two Players")
            else:
                await ctx.send(f":exclamation: {ctx.author.mention} Single Player Cannot Play with Himself/Herself, There must be Two Players")
    else:
        await ctx.send(f":exclamation: {ctx.author.mention} You are Using The Command Wrong, Use `>help tictactoe` to get help related with the Command")


tictactoehelp = ">tictactoe [First Player] <Second Player>"

@bot.command()
async def tttstop(ctx):
    global matches, gameBoards, chances, teamCode
    try:
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
    except Exception as e:
        print(e)
        pass
    

tttstophelp = ">tttstop"

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
                await message.channel.send(f"<@{player1}> <@{player2}> The TicTacToe Match is a Tie ;-;")

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

pollhelp = '>poll <question between ""> [options -> (Minimum 2 - Maximum 10) between ""]'

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

slaphelp = ">slap [member] [reason]"

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

killhelp = ">kill [member] [reason]"

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

punchhelp = ">punch [member] [reason]"

afkdata = {}
username = {}
reasontopic = {}

@bot.command()
async def afk(ctx, *, reason: Optional[str]=None):
    global afkdata, username, reasontopic

    if ctx.guild.id not in afkdata:
        afkdata[ctx.guild.id] = {}
    if ctx.author.id not in afkdata[ctx.guild.id]:
        afkdata[ctx.guild.id][ctx.author.id] = {}
    if "Afk" not in afkdata[ctx.guild.id][ctx.author.id]:
        afkdata[ctx.guild.id][ctx.author.id]["Afk"] = False

    # print(afkdata)

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

    afkdata[ctx.guild.id][ctx.author.id]["Afk"] = True
    # print(list(afkdata[ctx.guild.id].keys()))
    # print(afkdata)

afkhelp = ">afk [reason]"

@bot.listen()
async def on_message(message):   
    global afkdata, username, reasontopic
    # print(afkdata)
    if message.guild.id in afkdata:
        if message.author.id in afkdata[message.guild.id]:
            if "Afk" in afkdata[message.guild.id][message.author.id]:
                if afkdata[message.guild.id][message.author.id]["Afk"] == True:
                    afkdata[message.guild.id][message.author.id]["Afk"] = False
                    await message.channel.send(f"Afk Removed: {message.author.mention} You are no More Afk Now!")
                    try:
                        await message.author.edit(nick=username[message.author.id])
                    except:
                        pass
                    del username[message.author.id]
                    del reasontopic[message.author.id]
                    del afkdata[message.guild.id][message.author.id]

@bot.listen()
async def on_message(message):
    global afkdata, reasontopic
    # print(afkdata)
    # print(reasontopic)
    if message.guild.id not in afkdata:
        afkdata[message.guild.id] = {}
    if not message.author.bot:
        users = list(afkdata[message.guild.id].keys())
        print(users)
        for user in users:
            # print(user)
            if afkdata[message.guild.id][user]["Afk"] == True:
                if f"<@{user}>" in message.content:
                    await message.channel.send(f"Afk: {message.author.mention} He is Currently Afk | Reason: {reasontopic[user]}")
            else:
                # print("He is not afk")
                pass

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

rulehelp = ">rule <rule no.>"
   
@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="Server Rules", description="These are some Rules of this Server", color= embedTheme)
    embed.add_field(name="1. No Promotion",value="  type >rule 1 for more info",inline= False)
    embed.add_field(name="2. No Abuses",value="  type >rule 2 for more info",inline= False)
    embed.add_field(name="3. No Spamming",value="  type >rule 3 for more info",inline= False)
    embed.add_field(name="4. No Toxicity",value="  type >rule 4 for more info\n\n",inline= False)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

ruleshelp = ">rules"

@bot.command()
async def avatar(ctx, owner: Optional[discord.Member]=None):
    if owner is None:
        owner = ctx.author
    embed = discord.Embed(title="Avatar",color=embedTheme)
    embed.set_author(icon_url=owner.avatar_url,name=owner)
    embed.set_image(url=owner.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

avatarhelp = ">avatar [user]"

@bot.command()
async def vote(ctx):
    embed = discord.Embed(title="Vote For Tornax\t\t", color=embedTheme)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Click on Below Link", value="[Vote Now](https://top.gg/bot/832897602768076816/vote)", inline=False)
    embed.add_field(name="Rewards", value="Coming Soon", inline=False)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

votehelp = ">vote"

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f'Hey there! Thanks for Adding me in {guild.name}, Type `>help` to get All about me')

@bot.command()
async def info(ctx):
    Listedgreetings = ["Hello!","Hi!","Hey!","Heya!"]
    RandomGreetings = random.choice(Listedgreetings)
    embed = discord.Embed(title="My Information",description=f"{RandomGreetings} I am Tornax a Multi-Talented Discord Bot, Designed, Created and Configured by MrinalSparks\n\nCurrently I Am In : {len(list(bot.guilds))} Servers", color=embedTheme)
    await ctx.send(embed=embed)

infohelp = ">info"

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="About Tornax",description="Tornax is a Multi-Talented and Friendly Bot, Use Tornax for moderation, server managements, streams and giveaways now!", color=embedTheme)
    await ctx.send(embed=embed)

abouthelp = ">about"

helphelp = ">help [anycommand]"

@bot.command()
async def help(ctx, anycommand: Optional[str]=None):
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
        myEmbed.add_field(name="Management",value=" addrole, removerole, clean, gstart, gstatus, gstop, gpaticipate, gquit, info, about, join, leave, leaveserver, lock, slowmode, resetnick, setnick, unlock ", inline=False)
        myEmbed.add_field(name="Moderation",value=" kick, mute, warn, unmute, ban, unban ", inline=False)
        myEmbed.add_field(name="Fun",value=" slap, kill, punch, tictactoe, tttstop \n----------------------\n", inline=False)
        myEmbed.add_field(name="\n\n**Official Server**",value="----------------------\nJoin Our Official Server for More Commands and Help \n\n \t-> [Join Now](https://discord.gg/H3688EEpWr)\n----------------------\n\n > Server's Current Prefix is :   `>`\n > Command Usage Example :   `>info`\n\n----------------------", inline=False)
        myEmbed.add_field(name="Readme", value="`>help` Shows this Message, use `>help [command]` to get more information about that Command\n\n")
        myEmbed.set_footer(icon_url=bot.user.avatar_url,text=f"Made by {Creater}")
        await ctx.send(embed=myEmbed)
    else:
        content = ""

        if anycommand == "tell": content=tellhelp
        elif anycommand == "ping": content=pinghelp
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
        elif anycommand == "about": content=abouthelp
        elif anycommand == "vote": content=votehelp
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
        elif anycommand == "tictactoe": content=tictactoehelp
        elif anycommand == "tttstop": content=tttstophelp
        elif anycommand == "help": content=helphelp
        commandEmbed = discord.Embed(description=f"{content}",color=embedTheme)
        await ctx.send(embed=commandEmbed)

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
    if message.content.lower().startswith(">botservers"):
        servers = list(bot.guilds)
        print(servers)

@bot.listen()
async def on_message(message):
    message.content = message.content.lower()
    for word in restricted_words:
        if message.content.count(word)>0:
            await message.channel.purge(limit = 1)
            await message.channel.send(f":exclamation: The Word you are Using is Not Allowed in this Server {message.author.mention}",delete_after=8)

bot.run(TOKEN)