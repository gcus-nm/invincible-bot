# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:46:15 2022

@author: gcus_nm12
"""

import DiscordPi
import subprocess

import socket
from enum import IntEnum
from discord.ext import tasks
from discord.ext import commands
from mcrcon import MCRcon
import time


# ARKサーバー状態
class ArkServerState(IntEnum):
    VPS_SHUTDOWN = 1    #　サーバーが動いていない状態
    VPS_STARTING = 2    #　サーバー起動中
    VPS_RUNNING = 3     # サーバーは動いてるけどARKを起動していない状態
    ARK_STARTING = 4    # ARK起動中
    ARK_RUNNING = 5     # ARKサーバーが起動している状態
    ARK_STOPPING = 6    # ARK停止中
    VPS_STOPPING = 7    # サーバー停止中
    UNKNOUN = 99        # おかしい
    
# ARK設定
# サーバー状態
ark_server_state = ArkServerState.UNKNOUN
# ConoHa アドレス
conoha_server_address = '163.44.248.46'
# ConoHa SSHポート
conoha_ssh_port = 22
# ARK rconポート
ark_rcon_port = 27020
# ARK　adminパスワード
ark_admin_password = 2126
# ゲーム終了時にサーバーをおとすか
isArkServerShutdown = 1
# 前回接続情報
prevConnection = 76534639315283

class ArkCog(commands.Cog):

    @commands.Cog.listener(name='on_message')
    async def on_ready():
        #　サーバー接続チェック開始
        ArkCog.SurveillanceServer.start()
    
          
    # ARK ConoHa サーバー起動コマンド
    @commands.Cog.listener(name='on_message')
    async def arkstart(ctx):
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return     
        
        
        # チャンネルIDを保存
        DiscordPi.send_channel = ctx.message.channel
        
        global ark_server_state
        if ark_server_state >= ArkServerState.ARK_STARTING and ark_server_state != ArkServerState.UNKNOUN:
            print("ARK was started.")
            sendMessage = "ARKはすでに開始されています。"
            await DiscordPi.send_channel.send(sendMessage)
            return
        
        
        if ark_server_state >= ArkServerState.VPS_STARTING and ark_server_state != ArkServerState.UNKNOUN:
            ark_server_state = ArkServerState.ARK_STARTING
        
            # チャンネルにメッセージ送信
            sendMessage = "レンタルサーバーは起動しているので、ARKを開始します..."
            await DiscordPi.send_channel.send(sendMessage)
            
            print("ARK Server Start.")
            
            sshCommand = "osascript /Users/user/minecraft/Git/ArkServerStart.scpt"
            subprocess.run(sshCommand, shell=True)    
            
            ArkCog.ArkConnect.start()
        
        else:        
            ark_server_state = ArkServerState.VPS_STARTING
        
            # チャンネルにメッセージ送信
            sendMessage = "ARKのレンタルサーバーの起動を開始します..."
            await DiscordPi.send_channel.send(sendMessage)
            
            print("ARK ConoHa Server Start.")
        
            # サーバー起動
            startCommand = "osascript /Users/user/minecraft/Git/ConohaStart.scpt"
            subprocess.run(startCommand, shell=True)
        
            ArkCog.ConoHaStart.start()
        
    # ARK stopコマンド
    @commands.Cog.listener(name='on_message')
    async def arkstop(ctx, stopTime = 60, isServerShut = 1):
        
        global conoha_server_address
        global ark_rcon_port
        global ark_admin_password
        global isArkServerShutdown
        
        isArkServerShutdown = isServerShut
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
        
        # チャンネルIDを保存
        DiscordPi.send_channel = ctx.message.channel
        
        global ark_server_state
        if ark_server_state == ArkServerState.ARK_RUNNING:
            
            ark_server_state = ArkServerState.ARK_STOPPING
            print("Ark Server Stop.")
            stopMes = str(stopTime) + "秒後にARKサーバーを停止します。"
            with MCRcon(conoha_server_address, str(ark_admin_password), int(ark_rcon_port))as mcr:
                mcr.command("Broadcast Stop the server after " + str(stopTime) + " seconds.")
            await DiscordPi.send_channel.send(stopMes)
            
            time.sleep(stopTime)
            
            with MCRcon(conoha_server_address, str(ark_admin_password), int(ark_rcon_port))as mcr:
                mcr.command("Broadcast Stop the server.")            
            await DiscordPi.send_channel.send("停止を開始します...")
            
            time.sleep(3)
            
            with MCRcon(conoha_server_address, str(ark_admin_password), int(ark_rcon_port))as mcr:
                mcr.command("DoExit")
            
            ArkCog.ArkDisConnect.start()
            
        else:
            await DiscordPi.send_channel.send("ARKサーバーは起動していません。")
            
    # ARK commandコマンド
    @commands.Cog.listener(name='on_message')
    async def arkcommand(ctx, *, cmd = "None"):   
        
        global conoha_server_address
        global ark_admin_password
        global ark_rcon_port
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
        
        # 送られてきたチャンネルを保存
        DiscordPi.send_channel = ctx.message.channel
        
        # コマンドが指定されてない
        if cmd == "None":        
            await DiscordPi.send_channel.send("コマンドを入力してください。 （例） #arkcommand DoExit")
            return
            
        global ark_server_state
        if ark_server_state == ArkServerState.ARK_RUNNING:
                   
            with MCRcon(str(conoha_server_address), str(ark_admin_password), int(ark_rcon_port))as mcr:
                mcr.command(str(cmd))
                
            if cmd == "DoExit":
                ArkCog.ArkDisConnect.start()
        else:
            await DiscordPi.send_channel.send("サーバーが起動していないのでコマンドを送信出来ませんでした。")
            
    # ARK commandコマンド
    @commands.Cog.listener(name='on_message')
    async def arksay(ctx, *, say = ""):   
        
        global conoha_server_address
        global ark_admin_password
        global ark_rcon_port
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
        
        # 送られてきたチャンネルを保存
        DiscordPi.send_channel = ctx.message.channel
            
        global ark_server_state
        if ark_server_state == ArkServerState.ARK_RUNNING:
            
            with MCRcon(str(conoha_server_address), str(ark_admin_password), int(ark_rcon_port))as mcr:
                mcr.command("Broadcast " + str(say))
            
        else:
            await DiscordPi.send_channel.send("サーバーが起動していないので発言できませんでした。")    
                
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
            stat = DiscordPi.discord.Game(name=runServerText)
            await DiscordPi.client.change_presence(status=DiscordPi.discord.Status.online, activity=stat)
            
            # 前回は接続できなかった場合
            if (prevConnection != result and prevConnection != 76534639315283):
                print("Server Running.")
                await DiscordPi.send_channel.send("サーバーが起動しました！")
                           
            
        # 接続失敗
        else:        
            # 接続
            isServerRun = False
            
            # Botのステータス変更
            stat = DiscordPi.discord.Game(name="#start でサーバーを起動できます　")
            await DiscordPi.client.change_presence(status=DiscordPi.discord.Status.idle, activity=stat)
            
            # 前回は接続できていた場合
            if (prevConnection != result and prevConnection != 76534639315283):
                print("Server Stopped.")
                await DiscordPi.send_channel.send("サーバーが停止しました。")
            
        # 今回の接続状況を保存
        prevConnection = result
        
        # 切断
        mySocket.close()
        
    
    # ARKサーバー（ConoHa）が立ったかチェック
    @tasks.loop(seconds=5)
    async def ConoHaStart():
        
        global conoha_server_address
        global conoha_ssh_port
        global ark_server_state
            
        # 接続テスト（ssh）
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((conoha_server_address, int(conoha_ssh_port)))
        
        # 接続成功
        if result == 0:
        
            ark_server_state = ArkServerState.ARK_STARTING
            # チャンネルにメッセージ送信
            print("ARK ConoHa Server Done.")
            sendMessage = "ARKのレンタルサーバーが起動しました！\nARKを起動します..."
            await DiscordPi.send_channel.send(sendMessage)
            # sshで起動
            print("ARK Server Start.")
            sshCommand = "osascript /Users/user/minecraft/Git/ArkServerStart.scpt"
            subprocess.run(sshCommand, shell=True)    
            
            ArkCog.ConoHaStart.stop()
            ArkCog.ArkConnect.start()
        
        # 切断
        mySocket.close()
        
    # ARKサーバー（ConoHa）シャットダウンチェック
    @tasks.loop(seconds=5)
    async def ConoHaStop():
        
        global conoha_server_address
        global conoha_ssh_port
        global ark_server_state
            
        # 接続テスト（ssh）
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((conoha_server_address, int(conoha_ssh_port)))
        
        # 接続失敗
        if result != 0:
        
            ark_server_state = ArkServerState.VPS_SHOTDOWN
            # チャンネルにメッセージ送信
            print("ConoHa Server Shutdown　done.")
            sendMessage = "ARKのレンタルサーバーがシャットダウンしました。"
            await DiscordPi.send_channel.send(sendMessage)
            
            ArkCog.ConoHaStop.stop()
        
        # 切断
        mySocket.close()
            
    # ARKに接続できるかチェック
    @tasks.loop(seconds=5)
    async def ArkConnect():
        
        global conoha_server_address
        global ark_rcon_port
        global ark_server_state
        
        # 接続テスト
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((conoha_server_address, int(ark_rcon_port)))
        
        # 接続成功
        if result == 0:
        
            ark_server_state = ArkServerState.ARK_RUNNING
            # チャンネルにメッセージ送信
            print("ARK Server Done.")
            sendMessage = "ARKが起動しました！（でも30秒ぐらい待ってね）"
            await DiscordPi.send_channel.send(sendMessage)
            ArkCog.ArkConnect.stop()
        
        # 切断
        mySocket.close()
        
    # ARK切断チェック
    @tasks.loop(seconds=5)
    async def ArkDisConnect(isShutdown = 1):
        
        global conoha_server_address
        global ark_rcon_port
        global isArkServerShutdown
        global ark_server_state
        
        # 接続テスト
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((conoha_server_address, int(ark_rcon_port)))
        
        # 接続できない
        if result != 0:
        
            # チャンネルにメッセージ送信
            print("ARK Server shutdown Done.")
            sendMessage = "ARKが終了しました。"
            
            if isArkServerShutdown != 1:          
                ark_server_state = ArkServerState.VPS_RUNNING  
                sendMessage += "\nレンタルサーバーのシャットダウンは行いません。"
                await DiscordPi.send_channel.send(sendMessage)
                ArkCog.ArkDisConnect.stop()
                return
                
            ark_server_state = ArkServerState.VPS_STOPPING
            sendMessage += "\nレンタルサーバーをシャットダウンします。"
            await DiscordPi.send_channel.send(sendMessage)
            
            # VM停止API
            print("ConoHa Server Shutdown.")
            sshCommand = "osascript /Users/user/minecraft/Git/ConoHaShutdown.scpt"
            subprocess.run(sshCommand, shell=True)   
            
            ArkCog.ArkDisConnect.stop()
            ArkCog.ConoHaStop.start()
        
        # 切断
        mySocket.close()