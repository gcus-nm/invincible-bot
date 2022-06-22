# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import socket
import discord.ext
from discord.ext import commands
from discord.ext import tasks
from mcrcon import MCRcon
import subprocess
import time

# デフォルトチャンネル　（今は開発用サーバーのチャンネル）
default_channel = 951654109788905502

# 送信先チャンネル
send_channel = 0

# 起動中テキスト
runServerText = "Minecraft Server"

server_wait_time = 60

# サーバー情報
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

# ARK設定
# ConoHa アドレス
conoha_server_address = '163.44.248.46'
# ConoHa SSHポート
conoha_ssh_port = 22
# ARK rconポート
ark_rcon_port = 27020
# ARK　adminパスワード
ark_admin_password = 2126
# ARKサーバー起動状態
isArkServerRun = False

client = commands.Bot(command_prefix='#')
prevConnection = 76534639315283


# Python（Bot）起動時
@client.event
async def on_ready():
    
    #　サーバー接続チェック開始
    SurveillanceServer.start()
    
    # 送信チャンネルのデフォルト設定
    global send_channel
    global default_channel
    
    send_channel = client.get_channel(default_channel)
    print("Bot Start.")
    
# commandコマンド
@client.command()
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
@client.command()
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
    
# stopコマンド
@client.command()
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
        
# ARK ConoHa サーバー起動コマンド
@client.command()
async def arkstart(ctx):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    
    # チャンネルにメッセージ送信
    print("ARK ConoHa Server Start.")
    sendMessage = "ARKのレンタルサーバーの起動を開始します..."
    await send_channel.send(sendMessage)
    
    # サーバー起動
    startCommand = "osascript /Users/user/minecraft/Git/ConohaStart.scpt"
    subprocess.run(startCommand, shell=True)
    
    ConoHaStart.start()
    
# ARK stopコマンド
@client.command()
async def arkstop(ctx, stopTime = 60):
    
    global conoha_server_address
    global ark_rcon_port
    global ark_admin_password
    global isArkServerRun
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    
    if isArkServerRun:
        print("Ark Server Stop.")
        stopMes = str(stopTime) + "秒後にARKサーバーを停止します。"
        with MCRcon(conoha_server_address, str(ark_admin_password), int(ark_rcon_port))as mcr:
            mcr.command("Broadcast Stop the server after" + str(stopTime) + "seconds.")
        await send_channel.send(stopMes)
        
        time.sleep(stopTime)
        
        with MCRcon(conoha_server_address, str(ark_admin_password), int(ark_rcon_port))as mcr:
            mcr.command("Broadcast Stop the server.")            
        await send_channel.send("停止を開始します...")
        
        time.sleep(3)
        
        with MCRcon(conoha_server_address, str(ark_admin_password), int(ark_rcon_port))as mcr:
            mcr.command("DoExit")
        
        ArkDisConnect.start()
        
    else:
        await send_channel.send("ARKサーバーは起動していません。")
        
# ARK commandコマンド
@client.command()
async def arkcommand(ctx, *, cmd = "None"):   
    
    global isArkServerRun
    global conoha_server_address
    global ark_admin_password
    global ark_rcon_port
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # 送られてきたチャンネルを保存
    global send_channel
    send_channel = ctx.message.channel
    
    # コマンドが指定されてない
    if cmd == "None":        
        await send_channel.send("コマンドを入力してください。 （例） #arkcommand DoExit")
        return
    
    if isArkServerRun:  
        
        with MCRcon(str(conoha_server_address), str(ark_admin_password), int(ark_rcon_port))as mcr:
            mcr.command(str(cmd))
        
    else:
        await send_channel.send("サーバーが起動していないのでコマンドを送信出来ませんでした。")
        
# ARK commandコマンド
@client.command()
async def arksay(ctx, *, say = ""):   
    
    global isArkServerRun
    global conoha_server_address
    global ark_admin_password
    global ark_rcon_port
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # 送られてきたチャンネルを保存
    global send_channel
    send_channel = ctx.message.channel
        
    if isArkServerRun:  
        
        with MCRcon(str(conoha_server_address), str(ark_admin_password), int(ark_rcon_port))as mcr:
            mcr.command("Broadcast " + str(say))
        
    else:
        await send_channel.send("サーバーが起動していないので発言できませんでした。")    
            
# サーバーとの接続が行えるか（サーバーが起動しているか）指定秒おきにチェック
@tasks.loop(seconds=5)
async def SurveillanceServer():
    
    # 前回の接続状況
    global prevConnection
    
    # サーバーアドレス
    global server_address
    
    # サーバーポート
    global server_port
    
    # 接続テスト
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((server_address, int(server_port)))
    
    global isServerRun
    # 接続成功
    if result == 0:
        # 接続
        isServerRun = True
        
        # ステータスメッセージ
        global runServerText
        
        # Botのステータス変更
        stat = discord.Game(name=runServerText)
        await client.change_presence(status=discord.Status.online, activity=stat)
        
        # 前回は接続できなかった場合
        if (prevConnection != result and prevConnection != 76534639315283):
            print("Server Running.")
            await send_channel.send("サーバーが起動しました！")
                       
        
    # 接続失敗
    else:        
        # 接続
        isServerRun = False
        
        # Botのステータス変更
        stat = discord.Game(name="#start でサーバーを起動できます　")
        await client.change_presence(status=discord.Status.idle, activity=stat)
        
        # 前回は接続できていた場合
        if (prevConnection != result and prevConnection != 76534639315283):
            print("Server Stopped.")
            await send_channel.send("サーバーが停止しました。")
        
    # 今回の接続状況を保存
    prevConnection = result
    
    # 切断
    mySocket.close()
    

# ARKサーバー（ConoHa）が立ったかチェック
@tasks.loop(seconds=5)
async def ConoHaStart():
    
    global conoha_server_address
    global conoha_ssh_port
    global isArkServerRun
        
    # 接続テスト（ssh）
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((conoha_server_address, int(conoha_ssh_port)))
    
    # 接続成功
    if result == 0:
    
        # チャンネルにメッセージ送信
        print("ARK ConoHa Server Done.")
        sendMessage = "ARKのレンタルサーバーが起動しました！\nARKを起動します..."
        await send_channel.send(sendMessage)
        # sshで起動
        print("ARK Server Start.")
        sshCommand = "osascript /Users/user/minecraft/Git/ArkServerStart.scpt"
        subprocess.run(sshCommand, shell=True)    
        
        isArkServerRun = True
        ConoHaStart.stop()
        ArkConnect.start()
    
    # 切断
    mySocket.close()
    
# ARKサーバー（ConoHa）シャットダウンチェック
@tasks.loop(seconds=5)
async def ConoHaStop():
    
    global conoha_server_address
    global conoha_ssh_port
    global isArkServerRun
        
    # 接続テスト（ssh）
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((conoha_server_address, int(conoha_ssh_port)))
    
    # 接続失敗
    if result != 0:
    
        # チャンネルにメッセージ送信
        print("ConoHa Server Shutdown　done.")
        sendMessage = "ARKのレンタルサーバーがシャットダウンしました。"
        await send_channel.send(sendMessage)
        
        isArkServerRun = False
        ConoHaStop.stop()
    
    # 切断
    mySocket.close()
        
# ARKに接続できるかチェック
@tasks.loop(seconds=5)
async def ArkConnect():
    
    global conoha_server_address
    global ark_rcon_port
    
    # 接続テスト
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((conoha_server_address, int(ark_rcon_port)))
    
    # 接続成功
    if result == 0:
    
        # チャンネルにメッセージ送信
        print("ARK Server Done.")
        sendMessage = "ARKが起動しました！（でも30秒ぐらい待ってね）"
        await send_channel.send(sendMessage)
        ArkConnect.stop()
    
    # 切断
    mySocket.close()
    
# ARK切断チェック
@tasks.loop(seconds=5)
async def ArkDisConnect():
    
    global conoha_server_address
    global ark_rcon_port
    
    # 接続テスト
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((conoha_server_address, int(ark_rcon_port)))
    
    # 接続できない
    if result != 0:
    
        # チャンネルにメッセージ送信
        print("ARK Server shutdown Done.")
        sendMessage = "ARKが終了しました。\nレンタルサーバーをシャットダウンします。"
        await send_channel.send(sendMessage)
        
        # VM停止API
        print("ConoHa Server Shutdown.")
        sshCommand = "osascript /Users/user/minecraft/Git/ConoHaShutdown.scpt"
        subprocess.run(sshCommand, shell=True)   
        
        ArkDisConnect.stop()
        ConoHaStop.start()
    
    # 切断
    mySocket.close()
    
client.run(os.environ.get('DISCORD_TOKEN'))
