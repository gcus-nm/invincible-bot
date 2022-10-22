# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:52:13 2022

@author: gcus_nm12
"""

import DiscordPi

import subprocess

from mcrcon import MCRcon

# 起動中テキスト
runServerText = "Minecraft Server"

server_wait_time = 60

# マイクラサーバー情報
# アドレス
server_address = 'gcus-MacPro.local'
# マイクラポート
server_port = 25024
# rconパスワード
rcon_password = 2126
# rconポート
rcon_port = 25025
# サーバー起動状態
isServerRun = False

# commandコマンド
@DiscordPi.client.command()
async def command(ctx, *, cmd = "None"):   
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # 送られてきたチャンネルを保存
    global send_channel
    send_channel = ctx.message.channel
    
    # コマンドが指定されてない
    if cmd == "None":        
        await send_channel.send("コマンドを入力してください。 （例） #command list")
        return
    
    global isServerRun
    if isServerRun:    
        # サーバーアドレス
        global server_address
        # rconパスワード
        global rcon_password
        # rconポート
        global rcon_port       
        
        with MCRcon(str(server_address), str(rcon_password), int(rcon_port))as mcr:
            res = mcr.command(str(cmd))
        
        await send_channel.send(res)
        
    else:
        await send_channel.send("サーバーが起動していないのでコマンドを送信出来ませんでした。")    

# startコマンド
@DiscordPi.client.command()
async def start(ctx, version = "1.18.1P", ram = 12):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # 送られてきたチャンネルを保存
    global send_channel
    send_channel = ctx.message.channel
    
    global isServerRun
    global isServerStartRequest
    
    if isServerRun:
        await send_channel.send("既にサーバーが起動しているため、起動できません。")
        return
    
    # javaバージョン
    javaVer = "17"
    
    # サーバーバージョンメッセージ
    versionMessage = "1.18.1"
    
    # Discordのステータスに表示する文字列
    global runServerText
    
    # 起動鯖のバージョン指定
    if  (version == "1.18.1" or version == "1.18.1P"):
        
        version = "1.18.1P"
        versionMessage = "1.18.1 バニラサーバー"
        runServerText = "1.18.1 バニラサーバー "
        javaVer = "17"
        
    elif (version == "1.12.2Mohist" or version == "takumi" or
        version == "Takumi" or version == "TAKUMI"):
        
        version = "1.12.2Mohist"
        versionMessage = "1.12.2 匠サーバー"
        runServerText = "1.12.2 匠サーバー "
        javaVer = "8"
        
    elif (version == "1.12.2SkyFactory4" or
          version == "sky" or version == "Sky" or 
          version == "skyfactory" or version == "SkyFactory"):
                
        version = "1.12.2SkyFactory4"
        versionMessage = "1.12.2 SkyFactory 4"
        runServerText = "1.12.2 SkyFactory 4 "
        javaVer = "8"

    elif (version == "1.19"):
        version = "1.19"
        versionMessage = "1.19"
        runServerText = "1.19"
        javaVer = "17"
    
    # チャンネルにメッセージ送信
    sendMessage = versionMessage + " の起動を開始します..."
    await send_channel.send(sendMessage)
    
    # 起動コマンドをシェルで起動
    print("Minecraft Server Start.")
    command = "osascript /Users/user/minecraft/Git/BuildMac.scpt";
    command = command + " " + str(version) + " " + str(ram) + " " + str(javaVer)
    
    subprocess.run(command, shell=True)
    
# stopコマンド
@DiscordPi.client.command()
async def stop(ctx):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    
    # サーバーが起動しているか
    global isServerRun    
    
    if isServerRun:
        print("Minecraft Server Stop.")
        await send_channel.send("サーバーを停止します...")
        # サーバーアドレス
        global server_address
        # rconパスワード
        global rcon_password
        # rconポート
        global rcon_port       
        
        with MCRcon(str(server_address), str(rcon_password), int(rcon_port))as mcr:
            mcr.command("stop")
            
    else:
        await send_channel.send("サーバーは起動していません。")    