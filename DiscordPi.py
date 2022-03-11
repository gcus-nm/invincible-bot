# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import discord.ext
from discord.ext import commands
import subprocess

channel_id = 951654109788905502

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    await client.get_channel(channel_id).send("HELLO")

@client.command()
async def start(ctx):
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    stat = discord.Game(name="Minecraft Server")
    await client.change_presence(status=discord.Status.online, activity=stat)
    await ctx.message.channel.send("Start")
    #subprocess.call("cd")
    #subprocess.call(". minecraft/build.sh")

client.run(os.environ.get('DISCORD_TOKEN'))
print("Ready")