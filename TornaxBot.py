import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import random
from typing import Optional

from discord.ext.commands import has_permissions,has_role,MissingPermissions,MissingRole,CommandNotFound,CommandInvokeError
from discord.member import Member

bot = commands.Bot(command_prefix = ">",help_command=None)

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

@bot.event
async def on_member_join(member):
    if member.guild.id == LegendServer:
        role1 = discord.utils.get(member.guild.roles, id=875247780535345222)
        role2 = discord.utils.get(member.guild.roles, id=875259339072491541)
        await member.add_roles(role1)
        await member.add_roles(role2)

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
    if message.guild.id == LegendServer:
        if "start" in message.content.lower() and "smp" in message.content.lower():
            await message.add_reaction("<:nahi:869447646866202624>")

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
            if duration is not None and unit is not None:
                if unit == "s":
                    wait = 1 * duration 
                    embed = discord.Embed(description = f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Seconds **" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Seconds \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    dmAlert = f"You are Muted in the Server by an Admin for `{duration}` Seconds"if reason is None else f"You are Muted in the Server by an Admin for `{duration}`` Seconds\n\t With the Reason of {reason}"
                elif unit == "m":
                    wait = 60 * duration 
                    embed = discord.Embed(description = f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Minutes **" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention} for `{duration}` Minutes \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    dmAlert = f"You are Muted in the Server by an Admin for `{duration}` Minutes"if reason is None else f"You are Muted in the Server by an Admin for `{duration}`` Minutes\n\t With the Reason of {reason}"
                elif unit == "h":
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

@bot.command()
@commands.has_permissions(manage_guild=True)
async def leaveserver(ctx):
        await ctx.guild.leave()
        # await ctx.send(f"{ctx.author.mention} Sorry you don't have Access to use this Command")

leaveserverhelp = ">leaveserver"

@leaveserver.error
async def leaverserver_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

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
    GiveawayActive = False
    GiveawayChannel = None

    StartAnnounce = ""
    ParticipantsMsg = ""
    MembersList = ""

    Participants = {

    }

    @bot.command()
    @commands.has_role("Giveaway Handler")
    async def gstart(ctx, Channel:discord.TextChannel, prize:str, endtime:int, unit:str):
        global GiveawayActive, GiveawayChannel, StartAnnounce, MembersList, ParticipantsMsg
        try:
            if GiveawayActive == False:
                GiveawayActive = True
                GiveawayChannel = Channel
                listtostr = list(Participants.keys())
                members = str(listtostr)

                members = members.replace("'","") 
                members = members.replace("[","") 
                members = members.replace("]","")
                # await asyncio.sleep(int(endtime))

                if GiveawayActive ==True:
                    if unit == "s" or unit == "seconds":
                        wait = 1 * endtime
                        unitTime = "Seconds"
                    elif unit =="m" or unit == "minutes":
                        wait = 60 * endtime
                        unitTime = "Minutes"
                    elif unit == "h" or unit == "hours":
                        wait = 60 * 60 * endtime
                        unitTime = "Hours"

                    StartAnnounce = await ctx.send(f":loudspeaker:  Giveaway has been Started by {ctx.author.mention} and Will End After `{endtime}` {unitTime} :partying_face:")
                    ParticipantsMsg = await ctx.send(f":busts_in_silhouette: Participants - {MembersList}")

                if GiveawayActive == True:
                    await asyncio.sleep(wait)

                if GiveawayActive == True:
                    if len(Participants) == 0:
                        Participants["No One"] = "No one Participated"
                    winnerCode = random.choice(list(Participants.values()))
                    CodeOwner = [k for k, v in Participants.items() if v == winnerCode]
                    print(CodeOwner)
                    winnerName = str(CodeOwner[0])
                    winner = f"{winnerName} || {winnerCode}"

                    embed = discord.Embed(title=f":loudspeaker: Giveaway has been Finished :exclamation: :partying_face:\t ||{ctx.message.guild.default_role}||\n",color=embedTheme)
                    embed.add_field(name="Winner of the Giveaway",value=f"{winner}",inline=True)
                    embed.add_field(name="Prize",value=f"{prize}",inline=True)
                    embed.add_field(name="Participants",value=f"{MembersList}\n\n Please Contact with The Giveaway Host For the Prize of this Giveaway",inline=False)

                    await GiveawayChannel.send(embed=embed)
                    Participants.clear()
                    MembersList = ""
                    GiveawayActive = False
                    GiveawayChannel = None
            else:
                await ctx.send(":exclamation: A Giveaway is Already Active in this Server")
        except MissingRole:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}')

    @bot.command()
    async def gparticipate(ctx):
        global StartAnnounce, MembersList, ParticipantsMsg
        if GiveawayActive == True:
            if ctx.channel == GiveawayChannel:
                if ctx.author.name not in Participants:
                    code = random.randint(000000,999999)
                    if code in Participants:
                        code = random.randint(000000,999999)
                    Participants[ctx.author.name] = code

                    listtostr = list(Participants.keys())
                    members = str(listtostr)

                    members = members.replace("'","") 
                    members = members.replace("[","") 
                    members = members.replace("]","")
                    MembersList = members

                    await ctx.author.send(f":partying_face: You have Successfully Participated in the Giveaway and Your Special Code for The Giveaway is `{code}`")
                    await ctx.send(f"{ctx.author.mention} We Accepted your Request, Please Check your Dm", delete_after=15)
                    await ParticipantsMsg.edit(content=f":busts_in_silhouette: Participants - {MembersList}")
                else:
                    await ctx.send(f"{ctx.author.mention} You have Already Participated in the Giveaway, you cannot Participate again", delete_after=15)
        else:
            await ctx.send(":exclamation: There is No Giveaway Active in this Server")

    @bot.command()
    async def gquit(ctx):
        global StartAnnounce, MembersList, ParticipantsMsg
        if GiveawayActive == True:
            if ctx.channel == GiveawayChannel:
                if ctx.author.name in Participants:

                    del Participants[ctx.author.name]

                    listtostr = list(Participants.keys())
                    members = str(listtostr)

                    members = members.replace("'","") 
                    members = members.replace("[","") 
                    members = members.replace("]","")
                    MembersList = members

                    await ctx.send(f"{ctx.author.mention} You have Successfully Quitted the Giveaway", delete_after=15)
                    await ParticipantsMsg.edit(content=f":busts_in_silhouette: Participants - {MembersList}")
                else:
                    await ctx.send(f"{ctx.author.mention} You are Already not a Participant of this Giveaway", delete_after=15)
        else:
            await ctx.send(":exclamation: There is No Giveaway Active in this Server")
    
    @bot.command()
    @commands.has_role("Giveaway Handler")
    async def gstatus(ctx):
        try:
            if GiveawayActive:
                await ctx.send(f"A Giveaway is Currently Active in this Server \n Number of Participants :- {Participants}\n Giveaway Channel :- {GiveawayChannel}")
            else:
                await ctx.send(":exclamation: There is No Giveaway Active in this Server")
        except MissingRole:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}')

    @bot.command()
    @commands.has_role("Giveaway Handler")
    async def gstop(ctx):
        global GiveawayActive, Participants, GiveawayChannel, MembersList
        try:
            if GiveawayActive == True:
                GiveawayActive = False
                GiveawayChannel = None
                Participants.clear()
                MembersList = ""
                await ctx.send(f"Giveaway has been Stopped by {ctx.author.mention}")
            else:
                await ctx.send(":exclamation: There is No Giveaway Active in this Server")
        except MissingRole:
            await ctx.send(f':exclamation: You must have a Role "Giveaway Handler" {ctx.author.mention}')

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

timer = False

@bot.command()
async def timerstart(ctx, seconds:int, *, reason: Optional[str]=None):
    global timer
    if timer == False:
        timer = True
        started = await ctx.send(f"Timer has Started : `{seconds}`"if reason is None else f"{reason} `{seconds}`")
        while 0 < seconds < seconds+1:
            if timer == True:
                await asyncio.sleep(0.7)
                seconds-=1
                await started.edit(content=f"Timer has Started : `{seconds}`"if reason is None else f"{reason} `{seconds}`")
            else:
                break
        await asyncio.sleep(1)
        if timer == True:
            await started.edit(content=f"Timer has Stopped {ctx.author.mention}")
            timer = False
        else:
            await started.edit(content=f"Timer has Stopped {ctx.author.mention}")

    else:
        await ctx.send(f":exclamation: {ctx.author.mention} A Timer is already Running in this Server")

timerstarthelp = ">timerstart <seconds> [reason]"

@bot.command()
async def timerstop(ctx):
    global timer
    if timer == True:
        timer = False
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

@bot.command()
async def slap(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    if member is None:
        member = bot.user
    embed1 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Slapped {member.mention} **", color=embedTheme)
    embed2 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Slapped {member.mention} because {ctx.author.name} was Crazy **", color=embedTheme)
    embed3 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Slapped {member.mention} because {ctx.author.name} went Angry **", color=embedTheme)
    embed4 = discord.Embed(description=f"** Slapped: {ctx.author.mention} Jumped from High Place and Slapped {member.mention} **", color=embedTheme)
    allEmbeds = [embed1,embed2,embed3,embed4]
    choice = random.choice(allEmbeds)
    if reason is None:
        choice = random.choice(allEmbeds)
    else:
        arguments = [f"Slapped {member.mention}",f"Jumped from High Place and Slapped {member.mention}"]
        randomArgu = random.choice(arguments)
        choice = discord.Embed(description=f"** Slapped: {ctx.author.mention} {randomArgu} because {reason} **", color=embedTheme)
    await ctx.send(embed=choice)

slaphelp = ">slap [member] [reason]"

@bot.command()
async def kill(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    if member is None:
        member = bot.user
    embed1 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} **", color=embedTheme)
    embed2 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} for his Last Birth's Revenge **", color=embedTheme)
    embed3 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} because {ctx.author.name} went Mad **", color=embedTheme)
    embed4 = discord.Embed(description=f"** Killed: {ctx.author.mention} Killed {member.mention} by Knife **", color=embedTheme)
    embed5 = discord.Embed(description=f"** Killed: {ctx.author.mention} Shooted {member.mention} by Shotgun **", color=embedTheme)
    embed6 = discord.Embed(description=f"** Killed: {ctx.author.mention} Stabbed Knife to {member.mention} **", color=embedTheme)
    allEmbeds = [embed1,embed2,embed3,embed4,embed5,embed6]
    choice = random.choice(allEmbeds)
    if reason is None:
        choice = random.choice(allEmbeds)
    else:
        arguments = [f"Killed {member.mention}",f"Shooted {member.mention} by Shotgun",f"Stabbed Knife to {member.mention}",f"Pushed {member.mention} from High Building"]
        randomArgu = random.choice(arguments)
        choice = discord.Embed(description=f"** Killed: {ctx.author.mention} {randomArgu} because {reason} **", color=embedTheme)
    await ctx.send(embed=choice)

killhelp = ">kill [member] [reason]"

@bot.command()
async def punch(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    if member is None:
        member = bot.user
    embed1 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} **", color=embedTheme)
    embed2 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} because {ctx.author.name} was Crazy **", color=embedTheme)
    embed3 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} on his Nose **", color=embedTheme)
    embed4 = discord.Embed(description=f"** Punched: {ctx.author.mention} Punched {member.mention} in Voilence **", color=embedTheme)
    allEmbeds = [embed1,embed2,embed3,embed4]
    if reason is None:
        choice = random.choice(allEmbeds)
    else:
        arguments = [f"Punched {member.mention}",f"Punched on {member.mention}'s Nose",f"Punched {member.mention} in Voilence"]
        randomArgu = random.choice(arguments)
        choice = discord.Embed(description=f"** Punched: {ctx.author.mention} {randomArgu} because {reason} **", color=embedTheme)
    await ctx.send(embed=choice)  

punchhelp = ">punch [member] [reason]"

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

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f'Hey there! Thanks for Adding me in {guild.name}, Type `>help` to get All about me')

@bot.command()
async def info(ctx):
    Listedgreetings = ["Hello!","Hi!","Hey!","Heya!"]
    RandomGreetings = random.choice(Listedgreetings)
    embed = discord.Embed(title="My Information",description=f"{RandomGreetings} I am Tornax a Multi-Talented Discord Bot, Designed, Created and Configured by MrinalSparks", color=embedTheme)
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
    print(len(bot.all_commands))
    if anycommand is None:
        randomGreet = random.choice(["Hi","Hey","Hello"])
        myEmbed = discord.Embed(color = embedTheme)
        myEmbed.add_field(name=f"{randomGreet} There! I'm Tornax",value="A Multi-Talented and Friendly Bot, Use Tornax for Moderation, Server Managements, Streaming and Giveaways now!\n \n \t-> [Invite Tornax to your Server Now!](https://discord.com/api/oauth2/authorize?client_id=832897602768076816&permissions=0&scope=bot)")
        myEmbed.add_field(name=f"Commands — 37",value="----------------------\n",inline=False)
        myEmbed.add_field(name="Miscellaneous",value=" tell, ping, thought, avatar, react, rule, rules, solve, time, timerstart, timerstop ", inline=False)
        myEmbed.add_field(name="Management",value=" addrole, removerole, clean, gstart, gstatus, gstop, gpaticipate, gquit, info, join, leave, leaverserver, lock, resetnick, setnick, unlock ", inline=False)
        myEmbed.add_field(name="Moderation",value=" kick, mute, warn, unmute, ban, unban ", inline=False)
        myEmbed.add_field(name="Fun",value=" slap, kill, punch \n----------------------\n", inline=False)
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
        elif anycommand == "info": content=infohelp
        elif anycommand == "join": content=joinhelp
        elif anycommand == "leave": content=leavehelp
        elif anycommand == "leaveserver": content=leaveserverhelp
        elif anycommand == "lock": content=lockhelp
        elif anycommand == "unlock": content=unlockhelp
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
        elif anycommand == "help": content=helphelp
        commandEmbed = discord.Embed(description=f"{content}",color=embedTheme)
        await ctx.send(embed=commandEmbed)

@bot.listen()
async def on_message(message):
    message.content = message.content.lower()
    for word in restricted_words:
        if message.content.count(word)>0:
            await message.channel.purge(limit = 1)
            await message.channel.send(f":exclamation: The Word you are Using is Not Allowed in this Server {message.author.mention}",delete_after=8)

bot.run(TOKEN)