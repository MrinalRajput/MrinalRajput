from os import name
import warnings
import discord
from discord.ext import commands, tasks
from datetime import datetime
import datetime as dt
import asyncio
import random
import aiohttp
from typing import Optional
import json
import time
from discord.ext.commands.converter import EmojiConverter
from discord.ext.commands.errors import BadArgument, BotMissingPermissions
from discord.player import FFmpegPCMAudio
from mcstatus import MinecraftServer
import asyncpg
from PIL import Image, ImageDraw
from io import BytesIO
import wikipedia
from googlesearch import search
import topgg
from PyDictionary import PyDictionary
import pypokedex
from countryinfo.countryinfo import CountryInfo
import pycountry

from discord.ext.commands import BadArgument, MissingPermissions,MissingRole,CommandInvokeError, MissingAnyRole, BotMissingPermissions
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

    return [current_prefix[0], "tornax ", "Tornax ", "<@832897602768076816> ", "<@!832897602768076816> " , "<@832897602768076816>  ", "<@!832897602768076816>  "]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = load_prefix, case_insensitive=True, intents=intents,help_command=None)

TOKEN = "ODMyODk3NjAyNzY4MDc2ODE2.YHqeVg.yfzVgB8hHizDFH7hSMTORIv5weg"

embedTheme = discord.Color.from_rgb(255, 255, 0)

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(dsn="postgres://hedzjyheqxxogl:72fa047d2fa81a6c5b450f47e3ca399b59c642abb2f4308b43425b06dcc4cd15@ec2-34-239-55-93.compute-1.amazonaws.com:5432/df3v4ppmtmif7v")
    await bot.pg_con.execute("CREATE TABLE IF NOT EXISTS prefixes(guild_id bigint, prefix text)") 
    print("Connected Successfully To DataBase")

botstatus = discord.Status.online
botactivity = discord.Activity(type=discord.ActivityType.watching, name="Server Members | >help")

maintain1 = discord.Status.dnd
maintain2 = discord.Game(name="Maintenance")

@bot.event
async def on_ready():
    status = botstatus
    activity = botactivity
    await bot.change_presence(status=status, activity=activity)
    print("I m Ready!")

@bot.command()
async def setprefix(ctx, *, newPrefix:Optional[str]=None):
    if ctx.guild:
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
            if "chat" in channel.name.lower() or "general" in channel.name.lower():
                await bot.pg_con.execute("UPDATE prefixes SET prefix=$1 WHERE guild_id=$2",DEFAULT_PREFIX,guild.id)
                custom_prefix = await bot.pg_con.fetchrow("SELECT prefix FROM prefixes WHERE guild_id = $1", guild.id)
                await channel.send(f'Hey there! Thanks for Adding me in {guild.name}, Type `{custom_prefix[0]}help` to get All about me \n <a:doublearrow:899299966957256745>  My Auto Functions and Stuff i Can do Automatically \n\t <a:doublearrow:899299966957256745> Welcome and Bye Messages \n\t <a:doublearrow:899299966957256745> Mod Logs of Warn, Mute, Ban etc. \n\t <a:doublearrow:899299966957256745> AutoModeration')
    # inviteChannel = bot.get_channel(890819215588741191)
    # inviteEmbed = discord.Embed(title = "Joined!", description=f"{bot.user.mention} Just Joined {guild.name}", color=embedTheme)
    # inviteEmbed.set_thumbnail(url=guild.icon_url)
    # inviteEmbed.add_field(name="Guild Owner", value=f"<@{guild.owner_id}>",inline=False)
    # inviteEmbed.add_field(name="Guild Members", value=f"#{guild.member_count}",inline=False)
    # inviteEmbed.add_field(name="Guild ID", value=guild.id,inline=False)
    # await inviteChannel.send(embed=inviteEmbed)

mutelist = {}

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if "welcome" in channel.name.lower() or "join" in channel.name.lower():
            created_at = member.created_at.strftime("%a, %d %b %Y %I:%M %p")
            joined_at = member.joined_at.strftime("%a, %d %b %Y %I:%M %p")
            welcomeEmbed = discord.Embed(title="Welcome!", description=f"A Member Just Joined **{member.guild.name}**",color=embedTheme)
            welcomeEmbed.set_thumbnail(url=member.avatar_url)
            welcomeEmbed.add_field(name="Member Joined", value=f"{member.mention}",inline=True)
            welcomeEmbed.add_field(name="Member Id", value=f"{member.id}", inline=True)
            welcomeEmbed.add_field(name="Joined Discord", value=f"{created_at}", inline=False)
            welcomeEmbed.add_field(name=f"Joined {member.guild.name}", value=f"{joined_at}", inline=True)
            welcomeEmbed.add_field(name=f"Member Number", value=f"#{member.guild.member_count}", inline=True)
            try:
                await channel.send(embed=welcomeEmbed)
            except:
                pass
    try:
        await member.send(embed=discord.Embed(title="Welcome", description="Hey! We Are So Excited to have you on team legends", color=embedTheme).set_thumbnail(url="https://emoji.discord.st/emojis/72af46cd-fdbd-4846-902c-62a97a9c7996.gif").add_field(name="Server",value=member.guild, inline=False).add_field(name="Member Number", value=f"#{member.guild.member_count}", inline=False))
    except:
        pass
    if member.guild.id in mutelist:
        if member.id in mutelist[member.guild.id]:
            try:
                mutedRole = discord.utils.get(member.guild.roles, name="Muted")
                await member.add_roles(mutedRole)
                for channel in member.guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False)
            except Exception as e:
                print(e)
                pass

@bot.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if "bye" in channel.name.lower() or "leave" in channel.name.lower():
            byeEmbed = discord.Embed(description=f"**Bye!**  {member.mention} Just Left {member.guild.name} Server",color=embedTheme)
            await channel.send(embed=byeEmbed)

@bot.event
async def on_dbl_vote(data):
    voteEmbed = discord.Embed(title="Voted!", description=f"{data}",color=embedTheme)
    # voteEmbed.add_field(name=f"Voter ID", value=f"{user.id}", inline=False)
    voteAnnounce = bot.get_channel(892260693846401054)
    # await user.send(f"Thanks For Voting {bot.user.mention} !! You Can get Rewards in Our Official Server - [Join](https://discord.gg/H3688EEpWr) ")
    await voteAnnounce.send(embed=voteEmbed)

@bot.listen()
async def on_message(message):
    if not message.author.bot:
        if message.content == "<@!832897602768076816>" or message.content == "<@832897602768076816>":
            prfx = await bot.pg_con.fetchrow("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
            emoji = "<a:dance_stickman:899174400132255844>"
            await message.add_reaction(emoji)
            await message.channel.send(f"My Prefix in {message.guild} is - `{prfx[0]}`")

async def modlogs(ctx, case, user, mod, timing, logreason, cased):
    for channel in ctx.guild.channels:
        if "mod" in channel.name.lower() or "mod-log" in channel.name.lower() or "server-log" in channel.name.lower():
            logEmbed = discord.Embed(title=f"Mod Logs", color=embedTheme)
            logEmbed.set_author(icon_url=ctx.guild.icon_url, name=f"{ctx.guild} || {case}")
            try:
                logEmbed.set_thumbnail(url=user.avatar_url)
                target="user"
            except:
                logEmbed.set_thumbnail(url=ctx.guild.icon_url)
                target="channel"
            if target == "user":logEmbed.add_field(name="User", value=user.mention, inline=True)
            elif target == "channel":logEmbed.add_field(name="Channel", value=user.mention, inline=True)

            logEmbed.add_field(name="Moderator", value=mod.mention, inline=True)
            if timing is not None:
                logEmbed.add_field(name="Period", value=timing, inline=True)
            logEmbed.add_field(name="Reason", value=logreason, inline=True)
            logEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"{cased} By {mod.name}")
            await channel.send(embed=logEmbed)

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
        if message.author != bot.user:
            channelid = 874904257265008670
            modmail = bot.get_channel(channelid)
            embed = discord.Embed(title=f"{message.author}", color=embedTheme)
            embed.add_field(name="Message\n",value=f"{message.content}\n\n--------------------------",inline=False)
            embed.set_footer(icon_url=message.author.avatar_url,text=f"ID -> {message.author.id}")
            await modmail.send(embed=embed)

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

###############################
#### All Servers Commands ####
############0##################

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Optional[discord.Member]=None, days: Optional[int]=None, *, reason:Optional[str]=None):
    try:
        if member is not None:
            memberId = member.id
            if days is not None:
                wait = days * 86400
                try:
                    embed = discord.Embed(description = f"** {member.mention} has been Banned Successfully by {ctx.author.mention} for `{days}` Days **" if reason is None else f"** {member.mention} has been Banned Successfully by {ctx.author.mention} for `{days}` Days \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    dmuser = discord.Embed(description = f"** You are Banned by an Admin from {ctx.guild.name} for `{days}` Days **" if reason is None else f"** You are Banned by an Admin from {ctx.guild.name} for `{days}` Days \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    await ctx.send(embed=embed)
                    await member.ban(reason=reason)
                    await member.send(embed=dmuser)
                    await modlogs(ctx, "Ban", member, ctx.author, f"{days} Day(s)" , reason, "Banned")
                    await asyncio.sleep(wait)
                    await ctx.guild.unban(memberId)
                    await modlogs(ctx, "Unban", member, bot.user, None, "Auto", "Unbanned")
                except Exception as e:
                    print(e)
                    await ctx.reply(f":exclamation: Failed to Ban {member} From {ctx.guild}")
            else:
                if not member.guild_permissions.administrator:
                    embed = discord.Embed(description = f"** {member.mention} has been Banned Successfully by {ctx.author.mention} **" if reason is None else f"** {member.mention} has been Banned Successfully by {ctx.author.mention} \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    dmuser = discord.Embed(description = f"** You are Banned by an Admin from {ctx.guild.name} **" if reason is None else f"** You are Banned by an Admin from {ctx.guild.name} \n\t With the Reason of :\t{reason}**",color=embedTheme)
                    await ctx.send(embed=embed)
                    await member.send(embed=dmuser)
                    await member.ban(reason=reason)
                    await modlogs(ctx, "Ban", member, ctx.author, None , reason, "Banned")
                else:
                    await ctx.reply(f":exclamation: You Cannot Ban an Admin")
        else:
            await ctx.reply(f"You must Specify the User to Ban")
    except Exception as e:
        print(e)
        await ctx.reply(f":exclamation: You don't have Permissions to do that!")

banhelp = f"ban <member> [days] [reason]"

@bot.command()
async def unban(ctx, memberid: Optional[int]=None):
    global embedContent
    try:
        if memberid is not None:
            if ctx.author.guild_permissions.ban_members:
                user = await bot.fetch_user(memberid)
                await ctx.guild.unban(user)
                embedContent = f"Unbanned : Successfully Unbanned {user} from {ctx.guild.name}"
                embed = discord.Embed(description=embedContent, color=embedTheme)
                await ctx.send(embed=embed)
                await modlogs(ctx, "Unban", user, ctx.author, None, None, "Unbanned")
            else:
                await ctx.reply(f":exclamation: You don't have Permissions to do that!'")
        else:
            await ctx.reply(f":exclamation: Please Specify The User By his/her ID to Unban")
    except BadArgument:
        await ctx.reply(f":exclamation: The Member is not in This Server Please Try Unbanning with his/her Id")

unbanhelp = f"unban <member id>"

@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: Optional[discord.Member]=None, duration: Optional[int]=None, unit: Optional[str]=None, *, reason: Optional[str]=None ):
    global mutelist
    try:
        try:
            if ctx.guild.id not in mutelist:
                mutelist[ctx.guild.id] = []
            if member is not None:
                if member != ctx.author:
                    if duration is None and unit is not None:
                        reason = unit
                        unit = None
                    mutedRole = discord.utils.get(ctx.message.guild.roles, name="Muted")
                    if not mutedRole:
                        mutedRole = await ctx.guild.create_role(name="Muted")

                        for channel in ctx.guild.channels:
                            await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False)
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
                            mutelist[ctx.guild.id].append(member.id)
                            await ctx.send(embed=embed,delete_after=15)
                            for channel in ctx.guild.channels:
                                await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False)
                            await member.send(dmAlert)
                            if "s" in unit: period = f"{duration} Seconds"
                            elif "m" in unit: period = f"{duration} Minute"
                            elif "h" in unit: period = f"{duration} Hour"
                            await modlogs(ctx, "Mute", member, ctx.author, period, reason, "Muted")
                            await asyncio.sleep(wait)
                            await member.remove_roles(mutedRole)
                            if member.id in mutelist[ctx.guild.id]:
                                mutelist[ctx.guild.id].remove(member.id)
                            await modlogs(ctx, "Unmute", member, bot.user, None, "Auto", "Unmuted")
                        else:
                            await ctx.reply(f":exclamation: You Cannot Mute an Admin")
                    else:
                        if not member.guild_permissions.administrator:
                            embed = discord.Embed(description=f"** {member.mention} has been Muted Successfully by {ctx.author.mention}**" if reason is None else f"** {member.mention} has been Muted Successfully by {ctx.author.mention}\n\t With the Reason of :\t{reason}**",color=embedTheme)
                            await member.add_roles(mutedRole)
                            mutelist[ctx.guild.id].append(member.id)
                            await ctx.send(embed=embed,delete_after=15)
                            for channel in ctx.guild.channels:
                                await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False)
                            await member.send(f"You are Muted in the Server by an Admin"if reason is None else f"You are Muted in the Server by an Admin\n\t With the Reason of {reason}")
                            await modlogs(ctx, "Mute", member, ctx.author, "None", reason, "Muted")
                        else:
                            await ctx.reply(f":exclamation: You Cannot Mute an Admin")
                else:
                    await ctx.reply(f":exclamation: You cannot Mute YourSelf")
            else:
                await ctx.reply(f"Please Specify the User to Mute")
        except Exception:
            pass
    except MissingPermissions:
        await ctx.reply(f":exclamation: You don't have Permissions to do that!")

mutehelp = f"mute <member> [duration] [unit = s,m,h] [reason]"

@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    global mutelist
    if member is not None:
        mutedRole = discord.utils.get(ctx.message.guild.roles, name="Muted")
        if mutedRole in member.roles:
            embed = discord.Embed(description=f"** {member.mention} has been Unmuted Successfully by {ctx.author.mention}**" if reason is None else f"** {member.mention} has been Unmuted Successfully by {ctx.author.mention}\n\t With the Reason of :\t{reason}**",color=embedTheme)
            await member.remove_roles(mutedRole)
            if member.id in mutelist[ctx.guild.id]:
                mutelist[ctx.guild.id].remove(member.id)
            await ctx.send(embed=embed,delete_after=15)
            await modlogs(ctx, "Unmute", member, ctx.author, None, reason, "Unmuted")
        else:
            embed = discord.Embed(description=f"** :exclamation: {member.mention} is Not Muted in this Server **",color=embedTheme)
            await ctx.send(embed=embed,delete_after=15)
    else:
        await ctx.reply(f"Please Specify the User to Unmute")

unmutehelp = f"unmute <member> [reason]"

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: Optional[discord.Member]=None, *, reason=None):
    if member is not None:
        await ctx.send(embed= discord.Embed(description=f"✅ Successfully Warned {member.mention}" if reason is None else f"✅ Successfully Warned {member.mention} \n\t Reason: {reason}",color=embedTheme))
        if reason is None:
            reason = "Not Specified"
        await modlogs(ctx, "Warn", member, ctx.author, None, reason, "Warned")
    else:
        await ctx.send(f"You must Specify the User whom you want to Warn")

warnhelp = f"warn <member> [reason]"

@warn.error
async def warn_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Optional[discord.Member]=None, *, reason=None):
    if member is not None:
        if member == ctx.author:
            await ctx.send(f":exclamation: You cannot Kick yourself {ctx.author.mention}")
        else:
            if not member.guild_permissions.administrator:
                await member.kick(reason=reason)
                await ctx.send(embed= discord.Embed(description=f"✅ Successfully Kicked {member.mention} from the Server" if reason is None else f"✅ Successfully Kicked {member.mention} from the Server \n\t Reason: {reason}",color=embedTheme))
                await member.send(f"You are Kicked by an Admin from {ctx.guild.name}"if reason is None else f"You are Kicked by an Admin from {ctx.guild.name} \n\t With the Reason of :\t{reason}")
                await modlogs(ctx, "Kick", member, ctx.author, None, reason, "Kicked")
            else:
                await ctx.reply(f":exclamation: Failed to Kick that User Because that User is Mod or Admin in this Server")
    else:
        await ctx.send(f"You must Specify the User whom you want to Kick from the Server")

kickhelp = f"kick <member> [reason]"

@kick.error
async def kick_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

@bot.command()
async def softban(ctx, member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    if ctx.guild:
        if member is not None:
            if ctx.author.guild_permissions.ban_members:
                if not member.guild_permissions.administrator:
                    await member.ban(reason=reason)
                    await ctx.send(embed= discord.Embed(description=f"✅ Successfully gave Softban to {member.mention}" if reason is None else f"✅ Successfully gave Softban to {member.mention} \n\t Reason: {reason}",color=embedTheme))
                    await ctx.guild.unban(member)
                    await modlogs(ctx, "Softban", member, ctx.author, None, reason, "Softbanned")
                else:
                    await ctx.reply(f"The User is Either Mod or Admin in this Server, I Cannot do that")
            else:
                await ctx.send(":exclamation: You don't have Permissions to do that")
        else:
            await ctx.reply(f":exclamation: You Must Specify the User")
    else:
        await ctx.send(f"This Only Works in a Server not in Dm")

softbanhelp = f"softban <member> [reason]"

@bot.command()
async def voicekick(ctx, member: Optional[discord.Member]=None):
    if ctx.guild:
        if member is not None:
            if ctx.author.guild_permissions.move_members:
                if not member.guild_permissions.administrator:
                    if member.voice:
                        await member.move_to(channel=None)
                        await ctx.message.add_reaction("✅")
                    else:
                        await ctx.reply(f"The User is not in any Voice Channel")
                else:
                    await ctx.reply(f"The User is Either Mod or Admin in this Server, I Cannot do that")
            else:
                await ctx.send(":exclamation: You don't have Permissions to do that")
        else:
            await ctx.reply(f":exclamation: You Must Specify the User")
    else:
        await ctx.send(f":exclamation: You can Only Use it in a Server")

voicekickhelp = f"voicekick <member>"

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: Optional[discord.Member]=None, *, newname):
    if member is None:
        member = ctx.author
    membername = member.name
    await member.edit(nick=newname)
    embed = discord.Embed(description=f"<a:checked:899643253882769530>  Changed {membername}'s Nickname to {newname}! ", color=embedTheme)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

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
    embed = discord.Embed(description=f"<a:checked:899643253882769530>  Removed {membername}'s Nickname Successfully! ", color=embedTheme)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
    await ctx.send(embed=embed)

resetnickhelp = f"resetnick [member]"

@resetnick.error
async def resetnick_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit:int, member: Optional[discord.Member]=None):
    if limit > 0:
        quantity = "Messages"
        if limit == 1:
            quantity = "Message"
        if member is None:
            await ctx.channel.purge(limit=limit+1)
            embed = discord.Embed(description=f"🗑️   Successfully Deleted {limit} {quantity} in this Channel", color=embedTheme)
        else:
            def check(message):
                return message.author == member
            await ctx.channel.purge(limit=limit+1, check=check)
            embed = discord.Embed(description=f"🗑️   Successfully Deleted {limit} {quantity} of {member.mention} in this Channel", color=embedTheme)
        await ctx.send(embed=embed,delete_after=5)
    else:
        embed = discord.Embed(description=f"Nothing Deleted in this Channel", color=embedTheme)
        await ctx.send(embed=embed,delete_after=5)    

cleanhelp = f"clean <limit> [member]"

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: Optional[discord.TextChannel]=None):
    if channel is None:
        channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages=False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(description=f"🔒 Locked {channel.mention} for Members", color=embedTheme)
    await ctx.send(embed=embed)
    await modlogs(ctx, "Lock", channel, ctx.author, None, None, "Locked")

lockhelp = f"lock [channel]"

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: Optional[discord.TextChannel]=None):
    if channel is None:
        channel = ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages=True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(description=f"🔓 Unlocked {channel.mention} for Members", color=embedTheme)
    await ctx.send(embed=embed)
    await modlogs(ctx, "Unlock", channel, ctx.author, None, None, "Unlocked")

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

# @bot.command()
# async def addemoji(ctx, name: Optional[str]=None):
#     if name is None:
#         await ctx.send(f"Please Enter a Name for your Emoji")
#         def check(message):
#             return message.author == ctx.author and message.channel == ctx.channel
#         try:
#             name = await bot.wait_for("message", check=check, timeout=30)
#         except:
#             await ctx.send(f"Your Time for Sending Name of the Emoji has Ended")
#             return False

#     await ctx.send(f"Please Send the Emoji itself here!")
#     try:
#         def check(message):
#             return message.author == ctx.author and message.channel == ctx.channel
#         emoji:discord.Emoji = await bot.wait_for("message", check=check, timeout=30)
#     except:
#         await ctx.send(f"Your 30 Seconds for Sending the Emoji has Ended")
#         return False
#     # try:
#     print(emoji.content)
#     print(type(emoji.content))
    
#     # img = await EmojiConverter().convert(ctx, emoji.content)
#     # img = BytesIO(await img.read())
#     await ctx.guild.create_custom_emoji(name = (name), image = emoji.content)
#     # except Exception as e:
#     #     await ctx.send(embed=discord.Embed(description=f":exclamation: **Failed to Upload that as a Emoji Please Check that;**\n\t- Server has Space to Upload an Emoji, \n\t- The file that you uploaded is an image/gif, \n\t- File is not above 256kb in size.", color=embedTheme))
#     #     print(e)
#     #     return False
#     await ctx.send(f"Successfully Added - {emoji}")


@bot.command()
async def thought(ctx, *, word):
    if " " in word:
        word = discord.Embed(description=f"You cannot use More than one Word",color=embedTheme)
        await ctx.send(embed=word,delete_after=8)
    else:
        embed = discord.Embed(title=f"\t{word.upper()}", color=embedTheme)
        await ctx.send(embed=embed)

thoughthelp = f"thought <word>"

####### Giveaway ######

def getperiod(timing):
    duration = []
    unit=[]
    for i in timing:
        try:
            k = 1+int(i)
            duration.append(i)
        except:
            unit.append(i)
    if "".join(unit).startswith("s"):
        period = "Seconds"
    elif "".join(unit).startswith("m"):
        period = "Minutes"
    elif "".join(unit).startswith("h"):
        period = "Hours"
    elif "".join(unit).startswith("d"):
        period = "Days"
    maintime = "".join(duration) + " " + period
    alagalag = maintime.split()
    return alagalag

def ending(seccs):
    now = dt.datetime.now()
    delta = dt.timedelta(seconds = int(seccs))
    t = now.time()
    k = (dt.datetime.combine(dt.date(1,2,3),t)+delta).time()
    lent = []
    for t in str(k):
        if len(lent) < 5:
            lent.append(t)
    return "".join(lent)

gActive = {}

@bot.command()
async def gstart(ctx, gchannel: Optional[discord.TextChannel]=None, duration: Optional[str]=None, *, name: Optional[str]=None):
    global gActive
    GiveawayRole = discord.utils.get(ctx.guild.roles, name="Giveaway Handler")
    if GiveawayRole in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
        if gchannel is None:
            gchannel = ctx.channel

        if duration is not None:
            if name is not None:
                if ctx.guild.id not in gActive:
                    gActive[ctx.guild.id] = {}
                endtime = int(getperiod(duration)[0])
                endunit = getperiod(duration)[1]
                thisactive = str(len(gActive[ctx.guild.id].keys())+1)
                while thisactive in gActive[ctx.guild.id]:
                    thisactive = str(int(thisactive)+1)
                gActive[ctx.guild.id][thisactive] = {}
                gActive[ctx.guild.id][thisactive]["status"] = True 
                gActive[ctx.guild.id][thisactive]["channel"] = gchannel 
                gActive[ctx.guild.id][thisactive]["host"] = ctx.author 
                gActive[ctx.guild.id][thisactive]["participants"] = []
                gActive[ctx.guild.id][thisactive]["name"] = name
                if endunit.startswith("S"): seccs = int(endtime)*1
                elif endunit.startswith("M"): seccs = int(endtime)*60
                elif endunit.startswith("H"): seccs = int(endtime)*60*60
                elif endunit.startswith("D"): seccs = int(endtime)*60*60*24

                giveawayEmbed = discord.Embed(color=embedTheme)
                giveawayEmbed.set_author(name=name.capitalize())
                giveawayEmbed.add_field(name="Ending Time", value=ending(str(seccs)))
                giveawayEmbed.add_field(name="Hosted By", value=ctx.author.mention)
                giveawayEmbed.set_image(url="https://t4.ftcdn.net/jpg/04/61/96/99/240_F_461969925_Lu8i7asFdzjUnlo2kSEa6Yrdg3wBHHJ0.jpg")
                giveawayEmbed.set_footer(text="React with 🎉 to Participate in the Giveaway")

                gActive[ctx.guild.id][thisactive]["message"] = await ctx.send(embed=giveawayEmbed)
                await gActive[ctx.guild.id][thisactive]["message"].add_reaction("🎉")

                await asyncio.sleep(seccs)
                if gActive[ctx.guild.id][thisactive]["status"] == True:
                    if len(gActive[ctx.guild.id][thisactive]["participants"]) > 0:
                        getwinner = random.choice(gActive[ctx.guild.id][thisactive]["participants"])
                        winner = await bot.fetch_user(getwinner)
                        winnername = winner.name
                        winnermention = winner.mention
                    else:
                        winner = "Nobody"
                        winnername = "Nobody"
                        winnermention = "Nobody"
                    giveawayEmbed = discord.Embed(color=embedTheme)
                    giveawayEmbed.set_author(name=name.capitalize())
                    giveawayEmbed.add_field(name="Ending Time", value="Ended!")
                    giveawayEmbed.add_field(name="Hosted By", value=ctx.author.mention)
                    giveawayEmbed.add_field(name="Winners", value=winnermention)
                    giveawayEmbed.set_image(url="https://t4.ftcdn.net/jpg/04/61/96/99/240_F_461969925_Lu8i7asFdzjUnlo2kSEa6Yrdg3wBHHJ0.jpg")
                    giveawayEmbed.set_footer(text=f"Winner - {winnername} | Host - {ctx.author.name}")
                    await gActive[ctx.guild.id][thisactive]["message"].edit(embed=giveawayEmbed)
                    if winnername != "Nobody":
                        await gActive[ctx.guild.id][thisactive]["message"].reply(f":tada:  Congratulations! {winnermention} Won {name.capitalize()} :partying_face:")
                    else:
                        await gActive[ctx.guild.id][thisactive]["message"].reply(f"Giveaway Ended! No One Participated in the Giveaway")
                    gActive[ctx.guild.id][thisactive]["status"] = False
            else:
                await ctx.reply(embed=discord.Embed(description=":exclamation: Please Keep a Name of Giveaway to Start!",color=embedTheme))
        else:
            await ctx.reply(embed=discord.Embed(description=":exclamation: Please Specify the Duration of the Giveaway!",color=embedTheme))     
    else:
        await ctx.reply(embed=discord.Embed(description="You Must Have a Role `Giveaway Handler` or `Manage Guild` Permissions to do that!", color=embedTheme))

gstarthelp = f"gstart [channel] <duration> <name>"

@bot.listen()
async def on_reaction_add(reaction, user):
    global gActive
    if not user.bot:
        thisgives = None
        for gives in gActive[reaction.message.guild.id].keys():
            if gActive[reaction.message.guild.id][gives]["message"].id == reaction.message.id:
                thisgives = gives
                gActive[reaction.message.guild.id][thisgives]["participants"].append(user.id)

@bot.listen()
async def on_reaction_remove(reaction, user):
    global gActive
    if not user.bot:
        thisgives = None
        for gives in gActive[reaction.message.guild.id].keys():
            if gActive[reaction.message.guild.id][gives]["message"] == reaction.message:
                thisgives = gives
                gActive[reaction.message.guild.id][thisgives]["participants"].remove(user.id)

@bot.command()
async def gstop(ctx, msg: Optional[discord.Message]=None):
    global gActive
    GiveawayRole = discord.utils.get(ctx.guild.roles, name="Giveaway Handler")
    if GiveawayRole in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
        if msg is not None:
            thisgives = None
            for gives in gActive[ctx.message.guild.id].keys():
                if gActive[ctx.message.guild.id][gives]["message"] == msg:
                    thisgives = gives
                    gActive[ctx.guild.id][thisgives]["status"] = False
                    await gActive[ctx.guild.id][thisgives]["message"].edit(embed=discord.Embed(color=embedTheme).set_author(name="The Giveaway has Stopped"))
        else:
            await ctx.reply(embed=discord.Embed(description="Please Mention the Giveaway by its Message ID!", color=embedTheme))
    else:
        await ctx.reply(embed=discord.Embed(description="You Must Have a Role `Giveaway Handler` or `Manage Guild` Permissions to do that!", color=embedTheme))

gstophelp = f"gstop <message id>"

@bot.command()
async def gstatus(ctx, msg: Optional[discord.Message]=None):
    global gActive
    GiveawayRole = discord.utils.get(ctx.guild.roles, name="Giveaway Handler")
    if GiveawayRole in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
        if msg is not None:
            thisgives = None
            for gives in gActive[ctx.message.guild.id].keys():
                if gActive[ctx.message.guild.id][gives]["message"] == msg:
                    thisgives = gives
                    embed=discord.Embed(color=embedTheme)
                    embed.set_author(name=f"Status for {gActive[ctx.guild.id][thisgives]['name']}")
                    embed.add_field(name="Participants", value=str(len(gActive[ctx.guild.id][thisgives]["participants"])))
                    embed.add_field(name="Channel", value=gActive[ctx.guild.id][thisgives]["channel"].mention)
                    embed.add_field(name="Hosted By", value=gActive[ctx.guild.id][thisgives]["host"].mention)
                    if gActive[ctx.guild.id][thisgives]["status"] == True:status="Active"
                    else:status="Ended!"
                    embed.add_field(name="Status", value=status)
                    await gActive[ctx.guild.id][thisgives]["message"].reply(embed=embed)
        else:
            await ctx.reply(embed=discord.Embed(description="Please Mention the Giveaway by its Message ID!", color=embedTheme))
    else:
        await ctx.reply(embed=discord.Embed(description="You Must Have a Role `Giveaway Handler` or `Manage Guild` Permissions to do that!", color=embedTheme))

gstatushelp = f"gstatus <message id>"

@bot.command()
async def greroll(ctx, msg: Optional[discord.Message]=None):
    global gActive
    GiveawayRole = discord.utils.get(ctx.guild.roles, name="Giveaway Handler")
    if GiveawayRole in ctx.author.roles or ctx.author.guild_permissions.manage_guild:
        if msg is not None:
            thisgives = None
            for gives in gActive[ctx.message.guild.id].keys():
                if gActive[ctx.message.guild.id][gives]["message"] == msg:
                    thisgives = gives
                    if gActive[ctx.guild.id][thisgives]["status"] == False:
                        if len(gActive[ctx.guild.id][thisgives]["participants"]) > 0:
                            getwinner = random.choice(gActive[ctx.guild.id][thisgives]["participants"])
                            winner = await bot.fetch_user(getwinner)
                            await gActive[ctx.guild.id][thisgives]["message"].reply(f":tada: Congratulations! {winner.mention} is the New Winner of the Giveaway {gActive[ctx.guild.id][thisgives]['name']}")
                        else:
                            await ctx.reply(f"The Giveaway Ended without Enough Participants!")
                    else:
                        await gActive[ctx.guild.id][thisgives]["message"].reply(f"{ctx.author.mention} Unable to Reroll, The Giveaway is Currently Active")

        else:
            await ctx.reply(embed=discord.Embed(description="Please Mention the Giveaway by its Message ID!", color=embedTheme))
    else:
        await ctx.reply(embed=discord.Embed(description="You Must Have a Role `Giveaway Handler` or `Manage Guild` Permissions to do that!", color=embedTheme))

grerollhelp = f"greroll <message id>"

#######################

@bot.command()
async def react(ctx, chat:Optional[discord.Message]=None, emoji:Optional[str]=None):
    if ctx.author.guild_permissions.manage_messages:
        if emoji is not None:
            if chat is not None:
                message = chat
                await message.add_reaction(emoji)
            else:
                await ctx.reply(f"Please Specify the Message by its ID to React")
        else:
            await ctx.reply(f"Please Specify the Emoji to React")
    else:
        await ctx.reply(f":exclamation: You don't have Permissions to do that!'")


reacthelp = f"react <message id> <emoji>"

@bot.command()
async def clearreacts(ctx, chat: Optional[discord.Message]=None):
    if ctx.author.guild_permissions.manage_messages:
        if chat is not None:
            message = chat
            await message.clear_reactions()
        else:
            await ctx.reply(f"Please Specify the Message by its ID to Remove Reactions")
    else:
        await ctx.reply(f":exclamation: You don't have Permissions to do that!'")

clearreactshelp = f"clearreacts <message id>"

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

# @bot.command()
# async def play(ctx, *, songtitle):
#     old = songtitle
#     vc = await ctx.author.voice.channel.connect()
#     print(vc)
#     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
#     songtitle = songtitle + " song youtube"
#     searchsong = search(songtitle, num_results=5, lang="en", proxy=None)
#     print(searchsong)
#     audio = discord.FFmpegPCMAudio("Badla.mp3", **FFMPEG_OPTIONS)
#     print(searchsong[0], audio)
#     vc.play(audio)
#     vc.volume = 100
#     songEmbed = discord.Embed(title="Playing", description=f"Playing A Song for {old}", color=embedTheme)
#     await ctx.reply(embed=songEmbed)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: Optional[discord.Member]=None, role: discord.Role=None):
    if role is not None:
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
    else:
        await ctx.reply(f"Please Specify the Role by Mentioning it!")

addrolehelp = f"addrole [member] <role>"

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: Optional[discord.Member]=None, role: discord.Role=None):
    if role is not None:
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
    else:
        await ctx.reply(f"Please Specify the Role by Mentioning it!")

removerolehelp = f"removerole [member] <role>"

@bot.command()
async def solve(ctx, num1: Optional[str]=None, operation: Optional[str]=None, num2: Optional[str]=None):
    if num1 is not None and operation is not None and num2 is not None:
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
    else:
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
                mcEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
                await ctx.send(embed=mcEmbed)
            else:
                await ctx.reply("You can Search a Server by its Ip not by Name")
        else:
            await ctx.reply("You Must Specify the Server Whose Detail You want to See")
    except Exception as e:
        print(e)
        await ctx.reply(f"The Server You are Looking For Does Not Exist or is Currently Down, Recheck The Server IP")

mcserverhelp = f"mcserver <Minecaft Java Server Ip>"

@bot.command()
async def Wikipedia(ctx, *, search: Optional[str]=None):
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
    googleEmbed = discord.Embed(title="Google Results", color=embedTheme)
    googleEmbed.set_thumbnail(url="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png")
    googleEmbed.add_field(name=f"Results For {query} - {totalresult}", value=f"{finalresult}", inline=False)
    googleEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author}")
    await ctx.send(embed=googleEmbed)

googlehelp = f"google <Search Topic>"

videoCount = {}

@bot.command()
async def youtube(ctx, *, searching):
    if ctx.guild.id not in videoCount:
        videoCount[ctx.guild.id] = {}
    if ctx.author.id in videoCount[ctx.guild.id]:
        if "video" in videoCount[ctx.guild.id][ctx.author.id]:
            try:
                await videoCount[ctx.guild.id][ctx.author.id]["video"].clear_reactions()
            except:
                pass
                del videoCount[ctx.guild.id][ctx.author.id]
        
    old = searching
    searching = f"{searching} youtube"
    searchResult = search(searching, num_results=30, lang="en", proxy=None)
    validResults = []
    for r in searchResult:
        if r.startswith("https://www.youtube.com/watch?v"):
            validResults.append(r)
    videoCount[ctx.guild.id][ctx.author.id]= {}
    videoCount[ctx.guild.id][ctx.author.id]["count"] = 0
    if len(validResults) > 0:

        videoCount[ctx.guild.id][ctx.author.id]["video"] = await ctx.send(validResults[videoCount[ctx.guild.id][ctx.author.id]["count"]])

        controls = ["⏮️","◀️","⏹️","▶️","⏭️"]
        for c in controls:
            await videoCount[ctx.guild.id][ctx.author.id]["video"].add_reaction(c)
        def check(reaction, user):
            return reaction.message == videoCount[ctx.guild.id][ctx.author.id]["video"] and str(reaction.emoji) in controls and user.id == ctx.author.id

        while ctx.author.id in videoCount[ctx.guild.id]:
            try:
                controlemoji, user = await bot.wait_for("reaction_add", check=check, timeout=120)

                if controlemoji.emoji == controls[0]:
                    videoCount[ctx.guild.id][ctx.author.id]["count"] = 0
                    await videoCount[ctx.guild.id][ctx.author.id]["video"].edit(content=validResults[videoCount[ctx.guild.id][ctx.author.id]["count"]])
                elif controlemoji.emoji == controls[1]:
                    videoCount[ctx.guild.id][ctx.author.id]["count"] -= 1
                    if videoCount[ctx.guild.id][ctx.author.id]["count"] < 0:
                        videoCount[ctx.guild.id][ctx.author.id]["count"] = len(controls)
                    await videoCount[ctx.guild.id][ctx.author.id]["video"].edit(content=validResults[videoCount[ctx.guild.id][ctx.author.id]["count"]])
                elif controlemoji.emoji == controls[2]:
                    await videoCount[ctx.guild.id][ctx.author.id]["video"].clear_reactions()
                    validResults.clear()
                    del videoCount[ctx.guild.id][ctx.author.id]
                elif controlemoji.emoji == controls[3]:
                    videoCount[ctx.guild.id][ctx.author.id]["count"] += 1
                    if videoCount[ctx.guild.id][ctx.author.id]["count"] > len(controls):
                        videoCount[ctx.guild.id][ctx.author.id]["count"] = 0
                    await videoCount[ctx.guild.id][ctx.author.id]["video"].edit(content=validResults[videoCount[ctx.guild.id][ctx.author.id]["count"]])
                elif controlemoji.emoji == controls[4]:
                    videoCount[ctx.guild.id][ctx.author.id]["count"] = len(controls)
                    await videoCount[ctx.guild.id][ctx.author.id]["video"].edit(content=validResults[videoCount[ctx.guild.id][ctx.author.id]["count"]])
                
                if ctx.author.id in videoCount[ctx.guild.id]:
                    if "video" in videoCount[ctx.guild.id][ctx.author.id]:
                        await videoCount[ctx.guild.id][ctx.author.id]["video"].remove_reaction(controlemoji.emoji, user)
            except Exception as e:
                if ctx.author.id in videoCount[ctx.guild.id]:
                    if "video" in videoCount[ctx.guild.id][ctx.author.id]:
                        try:
                            await videoCount[ctx.guild.id][ctx.author.id]["video"].clear_reactions()
                        except Exception as e:
                            print(e)
                            pass
                        del videoCount[ctx.guild.id][ctx.author.id]
                        validResults.clear()
    else:
        await ctx.reply(f'''I didn't Found Result for "{old}" in Youtube''')

youtubehelp = f"youtube <Search Topic>"

@bot.command()
async def meaning(ctx, *, keyword: Optional[str]=None):
    if " " not in keyword:
        if keyword is not None:
            dictionary  = PyDictionary()
            result = dictionary.meaning(keyword.lower())
            if result is not None:
                embed = discord.Embed(title="Dictionary", description=f"**Results for - {keyword}**", color=embedTheme)
                embed.set_thumbnail(url="http://ragmamoul.net/wp-content/uploads/2019/08/3-Paligian.jpg")

                if len(result) == 1:
                    embed.add_field(name=f"[{len(list(result.values())[0])}] " + list(result.keys())[0], value= '• ' + '\n • '.join(list(result.values())[0]), inline=False)
                elif len(result) == 2:
                    embed.add_field(name=f"[{len(list(result.values())[0])}] " + list(result.keys())[0], value= '• ' + '\n • '.join(list(result.values())[0]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[1])}] " + list(result.keys())[1], value= '• ' + '\n • '.join(list(result.values())[1]), inline=False)
                elif len(result) == 3:
                    embed.add_field(name=f"[{len(list(result.values())[0])}] " + list(result.keys())[0], value= '• ' + '\n • '.join(list(result.values())[0]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[1])}] " + list(result.keys())[1], value= '• ' + '\n • '.join(list(result.values())[1]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[2])}] " + list(result.keys())[2], value= '• ' + '\n • '.join(list(result.values())[2]), inline=False)
                elif len(result) == 4:
                    embed.add_field(name=f"[{len(list(result.values())[0])}] " + list(result.keys())[0], value= '• ' + '\n • '.join(list(result.values())[0]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[1])}] " + list(result.keys())[1], value= '• ' + '\n • '.join(list(result.values())[1]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[2])}] " + list(result.keys())[2], value= '• ' + '\n • '.join(list(result.values())[2]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[3])}] " + list(result.keys())[3], value= '• ' + '\n • '.join(list(result.values())[3]), inline=False)
                else:
                    embed.add_field(name=f"[{len(list(result.values())[0])}] " + list(result.keys())[0], value= '• ' + '\n • '.join(list(result.values())[0]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[1])}] " + list(result.keys())[1], value= '• ' + '\n • '.join(list(result.values())[1]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[2])}] " + list(result.keys())[2], value= '• ' + '\n • '.join(list(result.values())[2]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[3])}] " + list(result.keys())[3], value= '• ' + '\n • '.join(list(result.values())[3]), inline=False)
                    embed.add_field(name=f"[{len(list(result.values())[4])}] " + list(result.keys())[4], value= '• ' + '\n • '.join(list(result.values())[4]), inline=False)
                    
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
                await ctx.send(embed=embed)
            else:
                await ctx.reply(f"I Didn't Found Meaning of {keyword} in Dictionary")
        else:
            await ctx.reply(f"Please Specify the Word for its Meaning")
    else:
        embed = discord.Embed(description=f"Please Try to Get Meaning of a Single Word",color=embedTheme)
        await ctx.send(embed=embed)        

meaninghelp = f"meaning <Word>"

@bot.command()
async def pokemon(ctx, pokename=None, wantmove: Optional[str]=None):
    if pokename is not None:
        nums = [1,2,3,4,5,6,7,8,9,0]
        try:
            if pokename not in nums:
                poke = pypokedex.get(name=pokename)
            else:
                poke = pypokedex.get(dex=pokename)
            if wantmove != "moves":
                pokeEmbed = discord.Embed(color= embedTheme)
                pokeEmbed.set_author(icon_url=poke.sprites[0]['default'], name=f"#{poke.dex} - {poke.name.capitalize()}")
                pokeEmbed.set_thumbnail(url=f"https://play.pokemonshowdown.com/sprites/ani/{poke.name}.gif")
                pokeEmbed.add_field(name="Type(s)", value=", ".join(poke.types).capitalize(), inline=True)
                pability = []
                pstats = f"HP: **{poke.base_stats[0]}**, ATK: **{poke.base_stats[1]}**, DEF: **{poke.base_stats[2]}**, SPA: **{poke.base_stats[3]}**, SPD: **{poke.base_stats[4]}**, SPE: **{poke.base_stats[5]}**"
                for ability in poke.abilities:
                    pability.append(ability.name.capitalize())
                pokeEmbed.add_field(name="Abilities", value=", ".join(pability), inline=True)
                pokeEmbed.add_field(name="Base Stats", value=pstats, inline=False)
                pokeEmbed.add_field(name="Base Exp", value=poke.base_experience, inline=True)
                pokeEmbed.add_field(name="Height", value=f"{poke.height * 10} cm", inline=True)
                pokeEmbed.add_field(name="Weight", value=f"{poke.weight / 10} kg", inline=True)
                pmoves = []
                allmove = poke.moves
                for move in allmove['ultra-sun-ultra-moon']:
                    if len(pmoves) < 6:
                        if move.name.capitalize() not in pmoves:
                            pmoves.append(move.name.capitalize())
                pokeEmbed.add_field(name=f"Moves[{len(pmoves)}]", value=f'{", ".join(pmoves)} \n\n Send `{ctx.prefix}pokemon {pokename} moves` for All Moves in DM', inline=True)
                pokeEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
                await ctx.send(embed=pokeEmbed)
            elif wantmove == "moves":
                moveEmbed = discord.Embed(color=embedTheme)
                moveEmbed.set_author(icon_url=poke.sprites[0]['default'], name=f"#{poke.dex} - {poke.name.capitalize()}")
                moveEmbed.set_thumbnail(url=f"https://play.pokemonshowdown.com/sprites/ani/{poke.name}.gif")
                pmoves = []
                allmove = poke.moves
                for move in allmove['ultra-sun-ultra-moon']:
                    if move.name.capitalize() not in pmoves:
                        pmoves.append(move.name.capitalize())
                moveEmbed.add_field(name=f"Moves[{len(pmoves)}]", value="\n".join(pmoves), inline=True)
                await ctx.author.send(embed=moveEmbed)
                if ctx.guild:
                    await ctx.send(embed=discord.Embed(description="Successfully Sent All Moves List, Please Check Your DM", color=embedTheme))
        except Exception as e:
            print(e)
            await ctx.reply(embed=discord.Embed(description=f"Pokemon {pokename} Not Found! Please Recheck the Name",color=embedTheme))
    elif pokename is None:
        await ctx.send(embed=discord.Embed(description=f"Please Specify the Pokemon you are Looking For!",color=embedTheme))

pokemonhelp = f"pokemon <Pokemon Name or Dex>"

@bot.command()
async def country(ctx, *, thecountry: Optional[str]=None):
    if thecountry is not None:
        try:
            query = CountryInfo(thecountry)
            countryEmbed = discord.Embed(title=query.name(), color=embedTheme)
            countryEmbed.set_thumbnail(url=f"https://www.worldometers.info/img/flags/small/tn_{query.iso()['alpha2']}-flag.gif")
            countryEmbed.add_field(name="Name", value=query.name(), inline=True)
            countryEmbed.add_field(name="Capital", value=query.capital(), inline=True)
            countryEmbed.add_field(name="ISO Code", value=query.iso()['alpha2'], inline=True)
            countryEmbed.add_field(name="Population", value=query.population(), inline=True)
            countryEmbed.add_field(name="Currency", value=", ".join(query.currencies()), inline=True)
            countryEmbed.add_field(name="TimeZone", value=", ".join(query.timezones()), inline=True)
            countryEmbed.add_field(name="SubRegion", value=query.subregion(), inline=True)
            countryEmbed.add_field(name="Area", value=query.area(), inline=True)
            countryEmbed.add_field(name="Calling Codes", value=", ".join(query.calling_codes()), inline=True)
            countryEmbed.add_field(name="Languages", value=", ".join(query.languages()), inline=True)
            countryEmbed.add_field(name="Demonym", value=query.demonym(), inline=True)
            countryEmbed.add_field(name="Country Latlng", value=query.latlng(), inline=True)
            countryEmbed.add_field(name="Capital Latlng", value=query.capital_latlng(), inline=True)
            countryEmbed.add_field(name="Alt Spelling(s)", value=", ".join(query.alt_spellings()), inline=True)
            countryEmbed.add_field(name=f"Country Capitals [{len(query.provinces())}]", value=f'{", ".join(query.provinces())} \n\n [Wikipedia]({query.wiki()}) || [Britannica](https://www.britannica.com/place/{query.name()})', inline=False)
            countryEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
            await ctx.send(embed=countryEmbed)
        except Exception as e:
            print(e)
            await ctx.reply(embed=discord.Embed(description=f"Country {thecountry} Doesn't Exist, Please Recheck the Spelling", color=embedTheme))
    else:
        await ctx.reply(f"Please Specify the Country You are Looking For!")

countryhelp = f"country <Country Name>"

@bot.command()
async def Time(ctx):
    currenttime = datetime.now()
    await ctx.send(f"Current Time is {currenttime}")

timehelp = f"time"

@bot.command()
async def tell(ctx, channel: Optional[discord.TextChannel]=None, *, msg):
    if ctx.guild:
        if channel is None:
            channel = ctx.channel
        if ctx.author.guild_permissions.administrator:
            await channel.send(msg)
        else:
            await ctx.reply(f"You don't have Permissions to do that, Only Admins Can Use the Command")

tellhelp = f"tell [channel] <message>"

triviaexist = {}
question = {"How many versions of 'Minecraft' are there?":["Two","2"],"Which equipment must you utilize to mine stone and ores in 'Minecraft'?":"Pickaxe","In Which Year was 'Minecraft' released?":"2011","How many slabs of iron ore are used to make one iron ingot?":["One","1"],"What can you wear to avoid Enderman ambushing you?":"Pumpkin","How tall is a Ghast (not including the tentacles)?":["Four","4"],"What ore can you construct complex machines with?":["RedStone","red stone"],"What vegetable can you wield to make a night vision mixture?":"golden carrot","Which real life animal was recorded to produce the sound effects of the Ghasts?":"cat","In which country is playing 'Minecraft' in school allowed?":"Sweden","How many days did it take to create the first version of 'Minecraft'?":["Six","6"],"How many night creatures can you find in 'Minecraft'?":["Five","5"],"In which version of the game were skeletons first introduced?":"alpha",'Who Is The "Feared Player" In Minecraft?':"Herobrine","Which Is The Most Important Block Type In Minecraft And Is Used To Make Everything Else?":"Wood","What Is The Name Of An Alternate World To Which You Can Travel?":["Nether","End"],"What Is The Smallest Animal In The Game?":"silverfish","How Far Away Can You Be From A Ghast For It To See You?":["100","Hundred"],"What Does The Creeper Mob Usually Drop After It Is Killed?":["GunPowder","gun powder"],"How Much Wool Is Required To Build A Bed?":["3","three"],"What Color Is The Default Skin's Shirt?":"Blue","Which Mob Never Drop An Item?":["Villager","SilverFish","bat","turtle"],"How Many Dyes Can Be Crafted?":["12","twelve"],"Which Was The First Enemy Introduced To ‘Minecraft’?":"Zombie","In A Full Set, How Many Pieces Of Armor Are There?":["4","four"],"How Many Items Are Required To Get An Active Conduit?":["3","three"],"Which Item Make A Creeper Explode Without It Noticing You?":"Flint and Steel","As Of The Aquatic Update, How Many Bad Mobs Are In The Game?":["32","thirty two"],"What Update Was The Phantom Released?":"1.6","During The Pretty Scary Update Which Hostile Mob Was Added?":"Witch","How many Different Types of Biomes are there in Minecraft?":["78","Seventy Eight"],"Which Type of Armor Cannot be Enchanted?":"horse","How many Health Points Does a Player Start with?":["20","Twenty"],"Which Mob Drop No Xp When Killed?":"bat","How many Types of Potions are Available to Players of Minecraft?":["32","thirty two"],"Which Mob was Accidentally Created While Trying to Make a Pig?":"creeper","Which Direction do Brewing Stands Always Face?":"East","What Color is the Bottle in a Brewing Stand after the Brewing Process?":"red","What's the Short Key to Clear Your Chat Spam?":["F3+D","F3 + D"],"How many Block Can a Stone Tool Mine Before Breaking?":"137","Below Which Depth Does One Typically Find Diamonds?":"15","What is the Maximum Enchantment Level in a Enchanting Table?":["30","thirty"],"How Much Gunpowder Do you Need to Craft a Tnt?":["5","Five"],"What is Notch's Real Name?":"Markus Persson","How Many Slots are there in a Double Chest?":"54","How Many Slots are there in a Single Chest?":"27","What is the Second Largest Mob in Minecraft?":"ghast","What is the Third Largest Mob in Minecraft?":"elder guardian","What is the Name of this Mob?":"Spider jockey","Which Mob is this?":"strider","What is the Name of this Underwater Mob?":"guardian","What is the Name of this Block?":"Prismarine","Which Block is this?":["Honeycomb","honey comb"],"Which Mob Gives the Item Shown in the Image When Killed?":"spider","What is the Name of this Monument or Building?":"fortress","What is the Name of this Biome in Minecraft?":"badlands","What is the Name of the Biome Shown in the Image?":"warm","How Much it Usually Cost to buy a Stack of Wool in Minecraft Bedwars?":["16","sixteen"],"What we Say if You kill a Player when his Bed is Broken in Minecraft Bedwars?":"final kill","What item do you get at the beginning of the game in Minecraft Bedwars?":"wooden sword","What the Defenders Defends in Minecraft Bedwars?":"bed"}
questionimg = {"What is the Name of this Mob?":"https://www.pngkit.com/png/full/375-3758344_minecraft-spider-jockey-spawn-egg-download-minecraft-spider.png","Which Mob is this?":"https://static.wikia.nocookie.net/minecraft/images/5/53/StriderWalking.gif/revision/latest/scale-to-width-down/162?cb=20200328203707","What is the Name of this Underwater Mob?":"https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/94/Guardian.gif/revision/latest/scale-to-width-down/250?cb=20190925152101","What is the Name of this Block?":"https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d9/Prismarine_JE2_BE2.gif/revision/latest/scale-to-width-down/150?cb=20190530002513","Which Block is this?":"https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/3b/Honeycomb_Block_JE1_BE1.png/revision/latest/scale-to-width-down/150?cb=20200124200218","Which Mob Gives the Item Shown in the Image When Killed?":"https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d8/Tripwire_%28NE%29.png/revision/latest/scale-to-width-down/150?cb=20190910132728","What is the Name of this Monument or Building?":"https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/cb/Nether_Fortress.png/revision/latest/scale-to-width-down/250?cb=20200415083830","What is the Name of this Biome in Minecraft?":"https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Badlands.png/revision/latest/scale-to-width-down/250?cb=20201108104745","What is the Name of the Biome Shown in the Image?":"https://static.wikia.nocookie.net/minecraft-biomes/images/2/24/Warm_Ocean_Coral_Reef.png/revision/latest/scale-to-width-down/382?cb=20180517172830"}
serverque = {}
participants = {}

@bot.command()
async def triviamc(ctx):
    global triviaexist, serverque, participants
    if ctx.guild.id not in triviaexist:
        triviaexist[ctx.guild.id] = False
    if ctx.guild.id not in participants:
        participants[ctx.guild.id] = {}
    if ctx.guild.id not in serverque:
        serverque[ctx.guild.id] = {}

    if triviaexist[ctx.guild.id] == False:
        donelist = []
        await ctx.send(embed=discord.Embed(title="❔ Trivia Mc Game", description=f"**Total Questions** - 6 \n Answering Time for Each Question - `15` Seconds)", color=embedTheme).set_footer(icon_url=ctx.author.avatar_url, text=f"Game By {ctx.author.name}"))
        await asyncio.sleep(2)
        triviaexist[ctx.guild.id] = True
        serverque[ctx.guild.id]["channel"] = ctx.channel
        serverque[ctx.guild.id]["1time"] = []
        serverque[ctx.guild.id]["points"] = 3
        while len(donelist) < 6:
            choosedque = random.choice(list(question.keys()))
            while choosedque in donelist:
                choosedque = random.choice(list(question.keys()))
            serverque[ctx.guild.id]["que"] = choosedque
            donelist.append(choosedque)
            if choosedque not in questionimg:
                await ctx.send(embed=discord.Embed(description=f"**{choosedque}**", color=embedTheme).set_author(icon_url=bot.user.avatar_url, name=f"# Question no. {len(donelist)}"))
            else:
                await ctx.send(embed=discord.Embed(description=f"**{choosedque}**", color=embedTheme).set_author(icon_url=bot.user.avatar_url, name=f"# Question no. {len(donelist)}").set_image(url=questionimg[choosedque]))
            await asyncio.sleep(10)
            serverque[ctx.guild.id]["1time"].clear()
            serverque[ctx.guild.id]["points"] = 3

        all = sorted(participants[ctx.guild.id].values())
        points = []
        for lt in all:
            points.append(str(lt))

        setup = []
        for i in points:
            for l in participants[ctx.guild.id]:
                if participants[ctx.guild.id][l] == int(i):
                    if l.name not in setup:
                        setup.append(l.name)
        points.reverse()
        setup.reverse()
        await ctx.send(embed=discord.Embed(title="Last Match Leaderboard 📋", color=embedTheme).add_field(name="Name", value="\n".join(setup)).add_field(name="Points", value="\n".join(points)))
        del triviaexist[ctx.guild.id]
        del serverque[ctx.guild.id]
        del participants[ctx.guild.id]
    else:
        await ctx.reply(f"A Trivia Game is Already Active in this Server")

triviamchelp = f"triviamc"

@bot.listen()
async def on_message(message):
    global serverque, participants
    if message.guild:
        if message.guild.id in triviaexist:
            if message.guild.id in serverque:
                if triviaexist[message.guild.id] == True:
                    if message.channel == serverque[message.guild.id]["channel"]:
                        if not message.author.bot:
                            if message.author.id not in serverque[message.guild.id]["1time"]:
                                if message.author not in participants[message.guild.id]:
                                    participants[message.guild.id][message.author] = 0
                                try:
                                    if question[serverque[message.guild.id]["que"]].lower() in message.content.lower():
                                        participants[message.guild.id][message.author] += serverque[message.guild.id]["points"]
                                        serverque[message.guild.id]["1time"].append(message.author.id)
                                        if serverque[message.guild.id]["points"] > 1:
                                            serverque[message.guild.id]["points"] -= 1
                                        print("correct")
                                except Exception as e:
                                    print(e)
                                    for x in question[serverque[message.guild.id]["que"]]:
                                        if x.lower() in message.content.lower():
                                            participants[message.guild.id][message.author] += serverque[message.guild.id]["points"]
                                            serverque[message.guild.id]["1time"].append(message.author.id)
                                            if serverque[message.guild.id]["points"] > 1:
                                                serverque[message.guild.id]["points"] -= 1
                                            print("correct")
                                            break

atlasgames = {}

@bot.command()
async def atlas(ctx, player1: Optional[discord.Member]=None, player2: Optional[discord.Member]=None, player3: Optional[discord.Member]=None, player4: Optional[discord.Member]=None):
    if ctx.guild.id not in atlasgames:
        atlasgames[ctx.guild.id] = []
    if player1 is None or player2 is None:
        await ctx.reply(f"There Must be Minimum 2 Players to Play Atlas Game")
    else:
        if player1.id not in atlasgames[ctx.guild.id] and player2.id not in atlasgames[ctx.guild.id]:
            atlasgames[ctx.guild.id].append(player1.id)
            atlasgames[ctx.guild.id].append(player2.id)
            if player3 is not None:
                atlasgames[ctx.guild.id].append(player3.id)
            if player4 is not None:
                atlasgames[ctx.guild.id].append(player4.id)

            turn = player1
            playersare = [player1.mention, player2.mention]
            if player3 is not None:
                playersare.append(player3.mention)
            if player4 is not None:
                playersare.append(player4.mention)

            places = []
            toldplaces = []
            for c in list(pycountry.countries):
                if c.name.lower() not in places:
                    places.append(c.name.lower())
            for s in list(pycountry.subdivisions):
                if s.name.lower() not in places:
                    places.append(s.name.lower())
            
            alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

            await ctx.send(f":map: Atlas Game :map:\n Players - {', '.join(playersare)}")

            if player1 is not None: isplayer1 = True
            else: isplayer1 = False
            if player2 is not None: isplayer2 = True 
            else: isplayer2 = False
            if player3 is not None: isplayer3 = True 
            else: isplayer3 = False
            if player4 is not None: isplayer4 = True 
            else: isplayer4 = False

            while True:
                playersare = [player1.mention, player2.mention]
                if player3 is not None:
                    playersare.append(player3.mention)
                if player4 is not None:
                    playersare.append(player4.mention)
                
                letter = random.choice(alphabets)
                await ctx.send(f"{turn.mention} Its Your Turn, You Have to tell a Country or State name Starts with `{letter}`")

                def check(message):
                    return message.author == turn and message.content.lower().startswith(letter) and message.channel == ctx.channel
                try:
                    userplace = await bot.wait_for("message", check=check, timeout=15)
                    if userplace.content.lower() in places and userplace.content.lower() not in toldplaces:
                        await userplace.reply(f"You Told Correct {userplace.content} is a Valid Place Starts With `{letter}`")
                        toldplaces.append(userplace.content.lower())
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            if isplayer3:
                                turn = player3
                            else:
                                turn = player1
                        elif turn == player3:
                            if isplayer4:
                                turn = player4
                            else:
                                turn = player1
                        elif turn == player4:
                            turn = player1

                    elif userplace.content.lower() in toldplaces:
                        await userplace.reply(f"{userplace.content} is Already Told by Someone")
                        playersare.remove(turn.mention)
                        await ctx.send(f"Loser - {turn.mention}\nWinners - {', '.join(playersare)}")
                        atlasgames[ctx.guild.id].remove(player1.id)
                        atlasgames[ctx.guild.id].remove(player2.id)
                        if player3 is not None:
                            atlasgames[ctx.guild.id].remove(player3.id)
                        if player4 is not None:
                            atlasgames[ctx.guild.id].remove(player4.id)
                        break
                    else:
                        await userplace.reply(f"You Told Incorrect Place, {userplace.content} is not a Country or State")
                        playersare.remove(turn.mention)
                        await ctx.send(f"Loser - {turn.mention}\nWinners - {', '.join(playersare)}")
                        atlasgames[ctx.guild.id].remove(player1.id)
                        atlasgames[ctx.guild.id].remove(player2.id)
                        if player3 is not None:
                            atlasgames[ctx.guild.id].remove(player3.id)
                        if player4 is not None:
                            atlasgames[ctx.guild.id].remove(player4.id)
                        break
                except Exception as e:
                    print(e)
                    await ctx.send(f"{turn.mention} Your Chance Timeout!")
                    playersare.remove(turn.mention)
                    await ctx.send(f"Loser - {turn.mention}\nWinners - {', '.join(playersare)}")
                    atlasgames[ctx.guild.id].remove(player1.id)
                    atlasgames[ctx.guild.id].remove(player2.id)
                    if player3 is not None:
                        atlasgames[ctx.guild.id].remove(player3.id)
                    if player4 is not None:
                        atlasgames[ctx.guild.id].remove(player4.id)
                    break        
        else:
            await ctx.reply(f"Anyone's Match is Currently Active")

atlashelp = f"atlas <player1> <player2> <player3> <player4>"

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
        randomRange = [0,10,20,30,40,50,60,70,80]
        gamingChannel[ctx.guild.id]["anyoneRange"] = random.choice(randomRange)
        gamingChannel[ctx.guild.id]["customRange"] = gamingChannel[ctx.guild.id]["anyoneRange"] + 20
        gamingChannel[ctx.guild.id]['secretNumber'] = random.randint(gamingChannel[ctx.guild.id]["anyoneRange"],gamingChannel[ctx.guild.id]["customRange"])
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
    if message.guild:
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
                            active[message.guild.id] = False
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

pollhelp = 'poll <question between ""> <options between "">'

@bot.command()
async def slap(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    # if member is None:
    #     member = bot.user
    slapemoji = ["<a:slaphen:899227046746652673>", "<a:pikaslap:899226900952670248>"]
    slapcurrent = random.choice(slapemoji)
    if member is not None:
        embed1 = discord.Embed(description=f"{slapcurrent} ** Slapped: {ctx.author.mention} Slapped {member.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"{slapcurrent} ** Slapped: {ctx.author.mention} Slapped {member.mention} because {ctx.author.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"{slapcurrent} ** Slapped: {ctx.author.mention} Slapped {member.mention} because {ctx.author.name} went Angry **", color=embedTheme)
        embed4 = discord.Embed(description=f"{slapcurrent} ** Slapped: {ctx.author.mention} Jumped from High Place and Slapped {member.mention} **", color=embedTheme)
    else:
        embed1 = discord.Embed(description=f"{slapcurrent} ** Slapped: {bot.user.mention} Slapped {ctx.author.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"{slapcurrent} ** Slapped: {bot.user.mention} Slapped {ctx.author.mention} because {bot.user.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"{slapcurrent} ** Slapped: {bot.user.mention} Slapped {ctx.author.mention} because {bot.user.name} went Angry **", color=embedTheme)
        embed4 = discord.Embed(description=f"{slapcurrent} ** Slapped: {bot.user.mention} Jumped from High Place and Slapped {ctx.author.mention} **", color=embedTheme)
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
            choice = discord.Embed(description=f"{slapcurrent} ** Slapped: {ctx.author.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
        else:
            choice = discord.Embed(description=f"{slapcurrent} ** Slapped: {bot.user.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
    await ctx.send(embed=choice)

slaphelp = f"slap [member] [reason]"

@bot.command()
async def kill(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    # if member is None:
    #     member = bot.user
    killemoji = ["<a:amongus_kill:899227736139259936>", "<a:pika_kill:899227835493928971>"]
    killcurrent = random.choice(killemoji)
    if member is not None:
        embed1 = discord.Embed(description=f"{killcurrent} ** Killed: {ctx.author.mention} Killed {member.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"{killcurrent} ** Killed: {ctx.author.mention} Killed {member.mention} for his Last Birth's Revenge **", color=embedTheme)
        embed3 = discord.Embed(description=f"{killcurrent} ** Killed: {ctx.author.mention} Killed {member.mention} because {ctx.author.name} went Mad **", color=embedTheme)
        embed4 = discord.Embed(description=f"{killcurrent} ** Killed: {ctx.author.mention} Killed {member.mention} by Knife **", color=embedTheme)
        embed5 = discord.Embed(description=f"{killcurrent} ** Killed: {ctx.author.mention} Shooted {member.mention} by Shotgun **", color=embedTheme)
        embed6 = discord.Embed(description=f"{killcurrent} ** Killed: {ctx.author.mention} Stabbed Knife to {member.mention} **", color=embedTheme)
    else:
        embed1 = discord.Embed(description=f"{killcurrent} ** Killed: {bot.user.mention} Killed {ctx.author.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"{killcurrent} ** Killed: {bot.user.mention} Killed {ctx.author.mention} for his Last Birth's Revenge **", color=embedTheme)
        embed3 = discord.Embed(description=f"{killcurrent} ** Killed: {bot.user.mention} Killed {ctx.author.mention} because {bot.user.name} went Mad **", color=embedTheme)
        embed4 = discord.Embed(description=f"{killcurrent} ** Killed: {bot.user.mention} Killed {ctx.author.mention} by Knife **", color=embedTheme)
        embed5 = discord.Embed(description=f"{killcurrent} ** Killed: {bot.user.mention} Shooted {ctx.author.mention} by Shotgun **", color=embedTheme)
        embed6 = discord.Embed(description=f"{killcurrent} ** Killed: {bot.user.mention} Stabbed Knife to {ctx.author.mention} **", color=embedTheme)
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
            choice = discord.Embed(description=f"{killcurrent} ** Killed: {ctx.author.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
        else:
            choice = discord.Embed(description=f"{killcurrent} ** Killed: {bot.user.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
    await ctx.send(embed=choice)

killhelp = f"kill [member] [reason]"

@bot.command()
async def punch(ctx,member: Optional[discord.Member]=None, *, reason: Optional[str]=None):
    # if member is None:
    #     member = bot.user
    punchemoji = ["<a:frog_punch:899261726246178866>", "<a:rage:899262299699818506>"]
    punchcurrent = random.choice(punchemoji)
    if member is not None:
        embed1 = discord.Embed(description=f"{punchcurrent} ** Punched: {ctx.author.mention} Punched {member.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"{punchcurrent} ** Punched: {ctx.author.mention} Punched {member.mention} because {ctx.author.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"{punchcurrent} ** Punched: {ctx.author.mention} Punched {member.mention} on his Nose **", color=embedTheme)
        embed4 = discord.Embed(description=f"{punchcurrent} ** Punched: {ctx.author.mention} Punched {member.mention} in Voilence **", color=embedTheme)
    else:
        embed1 = discord.Embed(description=f"{punchcurrent} ** Punched: {bot.user.mention} Punched {ctx.author.mention} **", color=embedTheme)
        embed2 = discord.Embed(description=f"{punchcurrent} ** Punched: {bot.user.mention} Punched {ctx.author.mention} because {bot.user.name} was Crazy **", color=embedTheme)
        embed3 = discord.Embed(description=f"{punchcurrent} ** Punched: {bot.user.mention} Punched {ctx.author.mention} on his Nose **", color=embedTheme)
        embed4 = discord.Embed(description=f"{punchcurrent} ** Punched: {bot.user.mention} Punched {ctx.author.mention} in Voilence **", color=embedTheme)

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
            choice = discord.Embed(description=f"{punchcurrent} ** Punched: {ctx.author.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
        else:
            choice = discord.Embed(description=f"{punchcurrent} ** Punched: {bot.user.mention} {randomArgu} Reason: {reason} **", color=embedTheme)
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

        if ctx.author not in afkdata[ctx.guild.id]:
            username[ctx.author.id] = ctx.author.nick
            if reason is None:
                reason = f"Nothing Specified"
            reasontopic[ctx.author.id] = reason
            await ctx.send(f"{ctx.author.mention} Afk Set : {reason}")
            try:
                await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")
            except:
                pass

            afkdata[ctx.guild.id].append(ctx.author.id)
        else:
            await ctx.send(f"{ctx.author.mention} You Afk has been Removed, User `>afk` Again to Set Your Afk")
    except Exception as e:
        print(e)
        pass

afkhelp = f"afk [reason]"

@bot.listen()
async def on_message(message):
    global afkdata, reasontopic
    # if not message.author.bot:
    if message.guild:
        if message.guild.id not in afkdata:
            afkdata[message.guild.id] = []
        users = afkdata[message.guild.id]
        if len(users) > 0:
            for user in users:
                username = await bot.fetch_user(user)
                if "@here" in message.content or "@everyone" in message.content:
                    pass
                else:
                    if username.mentioned_in(message):
                        if not message.author.bot:
                            if user in afkdata[message.guild.id]:
                                await message.channel.send(f"Afk: {username.name} is Currently Afk | Reason: {reasontopic[user]}")
                    else:
                        pass

@bot.listen()
async def on_message(message):   
    global afkdata, username, reasontopic
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
async def whois(ctx, member: Optional[discord.Member]=None):
    if ctx.guild:
        if member is None:
            member = ctx.author
        userEmbed = discord.Embed(description=member.mention, color=embedTheme)
        userEmbed.set_author(icon_url=member.avatar_url, name=member)
        userEmbed.set_thumbnail(url=member.avatar_url)
        userEmbed.add_field(name=f"Joined {ctx.guild.name}", value= member.joined_at.strftime("%a, %d %b %Y %H:%M %p"),inline=True)
        userEmbed.add_field(name=f"Joined Discord", value= member.created_at.strftime("%a, %d %b %Y %H:%M %p"),inline=True)
        if len(member.roles) > 1: 
            role_string = ' '.join([r.mention for r in member.roles][1:])
            userEmbed.add_field(name=f"Roles[{len(member.roles)-1}]", value= role_string,inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        userEmbed.add_field(name=f"Key Permissions", value= perm_string,inline=False)
        if member == ctx.guild.owner:
            userEmbed.add_field(name="Acknowledgements", value="Server Owner", inline=False)
        elif member.guild_permissions.administrator:
            userEmbed.add_field(name="Acknowledgements", value="Server Admin", inline=False)
        else:
            userEmbed.add_field(name="Acknowledgements", value="Server Member", inline=False)
        userEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
        await ctx.send(embed=userEmbed)
    else:
        await ctx.send(f":exclamation: This Command Only Works in a Server")

whoishelp = f"whois [user]"

@bot.command()
async def serverinfo(ctx):
    if ctx.guild:
        serverEmbed = discord.Embed(color=embedTheme)
        serverEmbed.set_author(icon_url=ctx.guild.icon_url, name=f"{ctx.guild.name}")
        serverEmbed.set_thumbnail(url=ctx.guild.icon_url)
        serverEmbed.add_field(name="Owner", value=ctx.guild.owner.mention, inline=True)
        serverEmbed.add_field(name="Channel Categories", value=len(ctx.guild.categories), inline=True)
        serverEmbed.add_field(name="Text Channels", value=len(ctx.guild.text_channels), inline=True)
        serverEmbed.add_field(name="Voice Channels", value=len(ctx.guild.voice_channels), inline=True)
        serverEmbed.add_field(name="Members", value=len(ctx.guild.members), inline=True)
        serverEmbed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        serverEmbed.add_field(name="ID", value=ctx.guild.id, inline=True)
        serverEmbed.add_field(name="Created at", value=ctx.guild.created_at.strftime("%a, %d %b %Y %I:%M %p"), inline=True)
        serverEmbed.add_field(name="Region", value=ctx.guild.region, inline=True)
        serverEmbed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}")
        await ctx.send(embed=serverEmbed)
    else:
        await ctx.send(f":exclamation: This Command Only Works in a Server")

serverinfohelp = f"serverinfo"

@bot.command()
async def emojis(ctx):
    serveremoji = []
    for emoji in ctx.guild.emojis:
        serveremoji.append(str(emoji))
    await ctx.send(embed=discord.Embed(title=f"{ctx.guild}'s Emojis [{len(ctx.guild.emojis)}]", description="  ".join(serveremoji) if len(ctx.guild.emojis) != 0 else "The Server doesn't Have any Emoji", color=embedTheme).set_footer(icon_url=ctx.author.avatar_url, text=f"Requested By {ctx.author.name}"))

emojishelp = f"emojis"

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
        myEmbed.add_field(name="Miscellaneous",value=" tell, poll, ping, afk, thought, vote, avatar, react, clearreacts, rule, rules, solve, time, timerstart, timerstop", inline=False)
        myEmbed.add_field(name="Management",value=" addrole, removerole, clean, allcommands, gstart, gstatus, gstop, greroll, setprefix, whois, emojis, serverinfo, info, invite, about, support, join, leave, lock, slowmode, resetnick, setnick, unlock ", inline=False)
        myEmbed.add_field(name="Moderation",value=" kick, mute, warn, unmute, ban, unban, softban, voicekick ", inline=False)
        myEmbed.add_field(name="Fun",value=" slap, kill, punch, wanted, tictactoe, tttstop, guess, atlas, triviamc, mcserver, wikipedia, google, youtube, meaning, pokemon, country \n----------------------\n", inline=False)
        myEmbed.add_field(name="\n\n**Official Server**",value=f"----------------------\nJoin Our Official Server for More Commands and Help \n\n \t-> [Join Now](https://discord.gg/H3688EEpWr)\n----------------------\n\n > Server's Current Prefix is :   `{ctx.prefix}`\n > Command Usage Example :   `{ctx.prefix}info`\n\n----------------------", inline=False)
        myEmbed.add_field(name="Readme", value=f"`{ctx.prefix}help` Shows this Message, use `{ctx.prefix}help [command]` to get more information about that Command and `{ctx.prefix}allcommands` for more information of all commands in detail - `<>` means Required and `[]` means Optional \n\n")
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
        elif anycommand == "clearreacts": content=clearreactshelp
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
        elif anycommand == "greroll": content=grerollhelp
        elif anycommand == "poll": content=pollhelp
        elif anycommand == "whois": content=whoishelp
        elif anycommand == "serverinfo": content=serverinfohelp
        elif anycommand == "emojis": content=emojishelp
        elif anycommand == "info": content=infohelp
        elif anycommand == "setprefix": content=setprefixhelp
        elif anycommand == "about": content=abouthelp
        elif anycommand == "vote": content=votehelp
        elif anycommand == "support": content=supporthelp
        elif anycommand == "wikipedia": content=wikipediahelp
        elif anycommand == "google": content=googlehelp
        elif anycommand == "youtube": content=youtubehelp
        elif anycommand == "meaning": content=meaninghelp
        elif anycommand == "join": content=joinhelp
        elif anycommand == "leave": content=leavehelp
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
        elif anycommand == "softban": content=softbanhelp
        elif anycommand == "voicekick": content=voicekickhelp
        elif anycommand == "slap": content=slaphelp
        elif anycommand == "kill": content=killhelp
        elif anycommand == "punch": content=punchhelp
        elif anycommand == "wanted": content=wantedhelp
        elif anycommand == "tictactoe": content=tictactoehelp
        elif anycommand == "tttstop": content=tttstophelp
        elif anycommand == "guess": content=guesshelp
        elif anycommand == "atlas": content=atlashelp
        elif anycommand == "triviamc": content=triviamchelp
        elif anycommand == "mcserver": content=mcserverhelp
        elif anycommand == "pokemon": content=pokemonhelp
        elif anycommand == "country": content=countryhelp
        elif anycommand == "allcommands": content=allcommandshelp
        elif anycommand == "help": content=helphelp
        else:
            content=None
        if content is not None:
            commandEmbed = discord.Embed(description=f"{ctx.prefix}{content}",color=embedTheme)
            await ctx.send(embed=commandEmbed)
        else:
            await ctx.reply(f"No Command Named `{ctx.prefix}{anycommand}`!")

activecmd = {}
cmdcode = {}

@bot.command()
async def allcommands(ctx):
    global activecmd, cmdcode
    if ctx.guild:
        if ctx.guild.id not in activecmd:
            activecmd[ctx.guild.id] = {}
        if ctx.guild.id not in cmdcode:
            cmdcode[ctx.guild.id] = {}

        if ctx.author.id in cmdcode[ctx.guild.id]:
            code = cmdcode[ctx.guild.id][ctx.author.id]
            try:
                await activecmd[ctx.guild.id][code]["message"].clear_reactions()
            except Exception as e:
                print(e)
                pass

        genCode = random.randint(000000, 999999)
        while genCode in activecmd[ctx.guild.id].keys():
            genCode = random.randint(000000, 999999)
        cmdcode[ctx.guild.id][ctx.author.id] = genCode
        activecmd[ctx.guild.id][genCode] = {}
        activecmd[ctx.guild.id][genCode]["page"] = 1

        sign = "→"

        toolsList = {f"{ctx.prefix}tell":"Send Your Message From Tornax for Announcements and Fun",f"{ctx.prefix}poll":"Easily Host Reaction Based Polls",f"{ctx.prefix}ping":"Get the Current Latency in ms value",f"{ctx.prefix}afk":"Let Others Know Your Status and What are You Doing Currently",f"{ctx.prefix}thought":"Show your Current Thinking in a Different & Higlighted Way",f"{ctx.prefix}avatar":"See Someone's Profile Picture/Avatar in Large Size",f"{ctx.prefix}whois":"Get All Details About an User of a Server",f"{ctx.prefix}react":"Let Tornax React on a Message for You",f"{ctx.prefix}clearreacts":"Remove/Clear All Reactions from a Message",f"{ctx.prefix}solve":"Use Tornax for Simple to Difficult Calculations",f"{ctx.prefix}timerstart":"Let Tornax Start Countdown for You",f"{ctx.prefix}timerstop":"Stop The Countdown in Between Started by Tornax"}
        toolscmd = []
        for cmd in list(toolsList.keys()):
            toolscmd.append(f"• {cmd} {sign}  {toolsList[cmd]}.")
        toolscmd = " \n ".join(toolscmd)

        toolsEmbed = discord.Embed(title="Tools Commands", description=f"{toolscmd} \n\n 1/8", color=embedTheme)

        managementList = {f"{ctx.prefix}addrole":"Give/Add Any Role to Anyone",f"{ctx.prefix}removerole":"Take/Remove Any Role From Anyone",f"{ctx.prefix}clean":"Clean/Delete So Many Messages of a User or Channel Quickly by Just Specifing the Quanitity",f"{ctx.prefix}setprefix":"Change Prefix of Tornax According to your Choice",f"{ctx.prefix}join":"Let Tornax Join a Voice Channel With You",f"{ctx.prefix}leave":"Let Tornax Leave a Voice Channel",f"{ctx.prefix}lock":"Lock any Channel of Your Server to Disallow Members to Send Messages in it",f"{ctx.prefix}unlock":"Unlock a Locked Channel of Your Server",f"{ctx.prefix}slowmode":"Set Slowmode for a Channel of Your Server",f"{ctx.prefix}setnick":"Set or Change Nick of YourSelf or any Member",f"{ctx.prefix}resetnick":"Reset/Remove Your or SomeBodies Nick"}
        managementcmd = []
        for cmd in list(managementList.keys()):
            managementcmd.append(f"• {cmd} {sign}  {managementList[cmd]}.")
        managementcmd = " \n ".join(managementcmd)
        managementEmbed = discord.Embed(title="Management Commands", description=f"{managementcmd} \n\n 2/8", color=embedTheme)
        
        giveawayList = {f"{ctx.prefix}gstart":"Start and Host a New Giveaway",f"{ctx.prefix}gstatus":"Get the Active Giveaway Status of Your Server",f"{ctx.prefix}gstop":"Stop a Giveaway in Between",f"{ctx.prefix}greroll":"Get a New Winner or Second Winner of a Giveaway"}
        giveawaycmd = []
        for cmd in list(giveawayList.keys()):
            giveawaycmd.append(f"• {cmd} {sign}  {giveawayList[cmd]}.")
        giveawaycmd = " \n ".join(giveawaycmd)
        giveawayEmbed = discord.Embed(title="Giveaways Commands", description=f"{giveawaycmd} \n\n 3/8", color=embedTheme)

        moderationList = {f"{ctx.prefix}kick":"Kick Anyone From Your Server",f"{ctx.prefix}mute":"Mute a Member of Your Server",f"{ctx.prefix}unmute":"Unmute a Muted Member in Your Server",f"{ctx.prefix}warn":"Warn a Member of Your Server With/Without a Reason",f"{ctx.prefix}ban":"Ban a Member from your Server Permanently or Temporary",f"{ctx.prefix}unban":"Unban a Banned Member in Your Server",f"{ctx.prefix}softban":"Ban a User and then Instantly Unban that user to Delete all his Messages with a Kick",f"{ctx.prefix}voicekick":"Kick a User from a Voice Channel"}
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

        minigamesList = {f"{ctx.prefix}tictactoe":"Challenge Your Friends for a Tictactoe Match",f"{ctx.prefix}tttstop":"Stop a Tictactoe Game in Between",f"{ctx.prefix}guess":"Start a Guess the Number Challenge with Your Server Members",f"{ctx.prefix}atlas":"Enjoy With Your Friends with Atlas Game and Recalling Some Countries",f"{ctx.prefix}triviamc":"Give Answers of Minecraft Quizes with Friends and Try to Achieve the Leaderboard"}
        minigamescmd = []
        for cmd in list(minigamesList.keys()):
            minigamescmd.append(f"• {cmd} {sign}  {minigamesList[cmd]}.")
        minigamescmd = " \n ".join(minigamescmd)
        minigamesEmbed = discord.Embed(title="Mini-Games Commands", description=f"{minigamescmd} \n\n 6/8", color=embedTheme)

        infoList = {f"{ctx.prefix}rule":"Get a Rule of a Server in Detail",f"{ctx.prefix}rules":"Get all Rules of a Server in a Listed and Proper Manner",f"{ctx.prefix}serverinfo":"Get Complete Detail and Information of a Server",f"{ctx.prefix}emojis":"Get All Emotes and Animated Emojis of a Server",f"{ctx.prefix}mcserver":"Get Status and Details of a Minecraft Java Server",f"{ctx.prefix}wikipedia":"Get a Biography or Informations in Details of a Particular Topic with Wikipedia",f"{ctx.prefix}google":"Get all Links Related With your Topic Quickly and in a Listed Manner",f"{ctx.prefix}youtube":"Search for Youtube Videos Fast and Efficiently",f"{ctx.prefix}meaning":"Get Meaning of Any Word Quickly and Easily",f"{ctx.prefix}pokemon":"Get All About of Your Favourite Pokemon in Detail",f"{ctx.prefix}country":"Get Full Information About a Country in Detail"}
        infocmd = []
        for cmd in list(infoList.keys()):
            infocmd.append(f"• {cmd} {sign}  {infoList[cmd]}.")
        infocmd = " \n ".join(infocmd)
        infoEmbed = discord.Embed(title="Information Commands", description=f"{infocmd} \n\n 7/8", color=embedTheme)

        generalList = {f"{ctx.prefix}info":"Get Information of Tornax in a brief way",f"{ctx.prefix}support":"Get Advantages, Details and Link of Our Official Server",f"{ctx.prefix}vote":"Get Tornax Voting Link with Rewards Information",f"{ctx.prefix}time":"Get the Current Time of Tornax",f"{ctx.prefix}invite":"Get a Link to Invite Tornax",f"{ctx.prefix}about":"Get Details and Information about Tornax with its Specialities",f"{ctx.prefix}help":"Get all Command's Names in a Quick and Brief Manner with Other Details ",f"{ctx.prefix}allcommands":"Shows this Embed Containing all Commands with Information in Details"}
        generalcmd = []
        for cmd in list(generalList.keys()):
            generalcmd.append(f"• {cmd} {sign}  {generalList[cmd]}.")
        generalcmd = " \n ".join(generalcmd)
        generalEmbed = discord.Embed(title="General Commands", description=f"{generalcmd} \n\n 8/8", color=embedTheme)

        print(len(toolsList.keys()) + len(managementList.keys()) + len(giveawayList.keys()) + len(moderationList.keys()) + len(funList.keys()) + len(minigamesList.keys()) + len(infoList.keys()) + len(generalList.keys()))

        await ctx.send(f"Each Page have One Category of Commands. If You have Problem with this and want Another way to get all Commands in brief way Try - `{ctx.prefix}help`")
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
    else:
        await ctx.send(f":exclamation: You Can Only Use this Command in a Server")

@bot.listen()
async def on_reaction_add(reaction, user):
    global cmdcode, activecmd
    try:
        if user.id != bot.user.id:
            if user.id in cmdcode[reaction.message.guild.id]:
                if user.id in cmdcode[reaction.message.guild.id]:
                    code = cmdcode[reaction.message.guild.id][user.id]
                    messge = activecmd[reaction.message.guild.id][code]["message"]
                    if reaction.message.id == messge.id:
                        if reaction.emoji == "🔢":
                            await messge.remove_reaction("🔢", user)
                            asking = await reaction.message.channel.send(f"In Which Page You Want to Jump?")
                            pages = ["1","2","3","4","5","6","7","8"]
                            def check(message):
                                return message.author.id == user.id and message.channel == reaction.message.channel  and message.content in pages

                            replymsg = await bot.wait_for(event="message",check=check,timeout=60)
                            if 0 < int(replymsg.content) < 9:
                                activecmd[reaction.message.guild.id][code]["page"] = int(replymsg.content)
                                await asking.delete()
                                await replymsg.delete()
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
                for thecode in activecmd[reaction.message.guild.id]:
                    if activecmd[reaction.message.guild.id][thecode]["message"].id == reaction.message.id:
                        await reaction.remove(user)
    except Exception as e:
        print(e)
        pass
                
count = {}

@bot.listen()
async def on_message(message):
    global count
    if message.guild:
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
            await asyncio.sleep(2600)
            count[message.guild.id][message.author.id]["warnings"] = 0

@bot.listen()
async def on_message(message):
    global count
    if message.guild:
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
                if not message.author.guild_permissions.administrator:
                    
                    if count[message.guild.id][message.author.id]["counting"] == True:
                        count[message.guild.id][message.author.id]["strikes"] += 1
                    if count[message.guild.id][message.author.id]["strikes"] > 3:
                        if count[message.guild.id][message.author.id]["warnings"] != 3:
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
                                for channel in message.guild.channels:
                                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False)
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
        await message.channel.send("<a:nachbe:899168499145015326>")
        servers = list(bot.guilds)
        print(servers)
        
restricted_words = ["harami","wtf","fuck","fuk","baap ","stfu"]

@bot.listen()
async def on_message(message):
    if message.guild:
        if not message.author.bot:
            if not message.author.guild_permissions.administrator:
                for word in restricted_words:
                    if word in message.content.lower():
                        await message.delete()
                        await message.channel.send(f":exclamation: The Word you are Using is Not Allowed in this Server {message.author.mention}",delete_after=8)
                
bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN)