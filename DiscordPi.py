# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import socket
import psutil
import discord.ext
from discord.ext import commands
from discord.ext import tasks
import subprocess
import sys

#channel_id = 951654109788905502

client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    SurveillanceServer.start()

@client.command()
async def start(ctx):
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    stat = discord.Game(name="Minecraft Server")
    await client.change_presence(status=discord.Status.online, activity=stat)
    await ctx.message.channel.send("サーバーを起動します...")
    subprocess.run(". /home/pi/minecraft/Git/build.sh", shell=True)
    
@tasks.loop(seconds=10)
async def SurveillanceServer():
    serverAdr = 'raspberrypi.local'
    port = 25565
    
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((serverAdr, int(port)))
    
    if result == 0:
        print("Connect!")
    else:
        print("Fail")
        
    mySocket.close()
    
    
client.run(os.environ.get('DISCORD_TOKEN'))