# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import discord.ext
import random
from discord.ext import commands
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('arg1')
args = parser.parse_args()

channel_id_server = 852963766630613032

client = commands.Bot(command_prefix='!')
channel = client.get_channel(channel_id_server)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)

@client.command()
async def start(ctx):
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    stat = discord.Game(name="Minecraft Server")
    await client.change_presence(status=discord.Status.online, activity=stat)
    await ctx.message.channel.send("Start コマンド")
    #subprocess.call("cd")
    #subprocess.call(". minecraft/build.sh")

client.run(os.environ.get('DISCORD_TOKEN'))