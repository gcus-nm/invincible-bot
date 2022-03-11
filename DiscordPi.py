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

# 特定のチャンネルID
channel_id = 951654109788905502

client = commands.Bot(command_prefix='#')
prevConnection = -1

# Python（Bot）起動時
@client.event
async def on_ready():
    
    #　サーバー接続チェック開始
    SurveillanceServer.start()

# startコマンド
@client.command()
async def start(ctx):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルにメッセージ送信
    await ctx.message.channel.send("サーバーの起動を開始します...")
    
    # 起動コマンドをシェルで起動
    subprocess.run(". /home/pi/minecraft/Git/build.sh", shell=True)
    
# サーバーとの接続が行えるか（サーバーが起動しているか）10秒おきにチェック
@tasks.loop(seconds=10)
async def SurveillanceServer():
    
    # 前回の接続状況
    global prevConnection
    
    # サーバーアドレス
    serverAdr = 'raspberrypi.local'    
    # ポート
    port = 25565
    
    # 接続テスト
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((serverAdr, int(port)))
    
    # 接続成功
    if result == 0:        
        print("Connect Server!")
        
        # 前回の接続ができなかった場合
        if (prevConnection != result):
            client.get_channel(channel_id).send("サーバーが起動しました！")
            
            # Botのステータス変更
            stat = discord.Game(name="Minecraft Server")
            await client.change_presence(status=discord.Status.online, activity=stat)
            
        
    # 接続失敗
    else:
        print("Connect Fail")
        
        # 前回は接続できていた場合
        if (prevConnection != result):
            client.get_channel(channel_id).send("サーバーが停止しました。")
            await client.change_presence(status=discord.Status.online, activity=None)
        
    # 今回の接続状況を保存
    prevConnection = result
    
    # 切断
    mySocket.close()
    
    
client.run(os.environ.get('DISCORD_TOKEN'))