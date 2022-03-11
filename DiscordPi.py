# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import discord.ext
from discord.ext import commands
import subprocess
import sys

channel_id = 951654109788905502

client = commands.Bot(command_prefix='#')

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
    await ctx.message.channel.send("サーバーを起動します...")
    subprocess.run(". /home/pi/minecraft/build.sh", shell=True)
    
input=sys.stdin.readline()
print(input)

client.run(os.environ.get('DISCORD_TOKEN'))