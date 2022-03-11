# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
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
    for proc in psutil.process_iter():
        print("----------------------")
        print("プロセスID:" + str(proc.pid))
    try:
        print("実行モジュール：" + proc.exe())
        print("コマンドライン:" + str(proc.cmdline()))
        print("カレントディレクトリ:" + proc.cwd())
    except psutil.AccessDenied:
        print("このプロセスへのアクセス権がありません。")
    
client.run(os.environ.get('DISCORD_TOKEN'))