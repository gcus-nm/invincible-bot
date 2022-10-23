# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import DiscordPi_ARK

import os
import subprocess

from discord.ext import commands

# デフォルトチャンネル　（今は開発用サーバーのチャンネル）
default_channel = 951654109788905502

# 送信先チャンネル
send_channel = 0

client = commands.Bot(command_prefix='#')

# Python（Bot）起動時
@client.event
async def on_ready():
    
    # 送信チャンネルのデフォルト設定
    global send_channel
    global default_channel
    
    send_channel = client.get_channel(default_channel)
    print("Bot Start.")
    
@client.command()
async def test(ctx):
        
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return      
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    # チャンネルにメッセージ送信
    print("Reboot.")
    await send_channel.send("サーバーPCの再起動を行います。")
    
# rebootコマンド
@client.command()
async def reboot(ctx):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    # チャンネルにメッセージ送信
    print("Reboot.")
    await send_channel.send("サーバーPCの再起動を行います。")
    
    # リブート
    subprocess.run("sudo reboot", shell=True)
  
    
client.run(os.environ.get('DISCORD_TOKEN'))
