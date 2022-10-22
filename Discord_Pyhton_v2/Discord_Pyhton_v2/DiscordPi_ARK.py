# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:46:15 2022

@author: gcus_nm12
"""

import subprocess
import discord
import socket
import time
from discord.ext import tasks, commands
from mcrcon import MCRcon
from enum import IntEnum

# ARKサーバー状態
class ArkServerState(IntEnum):
    VPS_SHUTDOWN = 1    # サーバーが動いていない状態
    VPS_STARTING = 2    # サーバー起動中
    VPS_RUNNING = 3     # サーバーは動いてるけどARKを起動していない状態
    ARK_STARTING = 4    # ARK起動中
    ARK_RUNNING = 5     # ARKサーバーが起動している状態
    ARK_STOPPING = 6    # ARK停止中
    VPS_STOPPING = 7    # サーバー停止中
    UNKNOUN = 99        # おかしいself
class ArkCog(commands.Cog):

    server_address = None
    server_port = None
    started_channel = None
    
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

    
    def __init__(self, bot, server_address, server_port):

        self.bot = bot
        self.server_address = server_address
        self.server_port = server_port

        ArkCog.SurveillanceServer.start(self)
          
    # ARK ConoHa サーバー起動コマンド
    @commands.command()
    async def arkstart(self, ctx):
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return     
        
        if self.ark_server_state >= ArkServerState.ARK_STARTING and self.ark_server_state != ArkServerState.UNKNOUN:
            print("ARK was started.")
            sendMessage = "ARKはすでに開始されています。"
            await ctx.message.channel.send(sendMessage)
            return
        else:
            self.started_channel = ctx.message.channel
        
        
        if self.ark_server_state >= ArkServerState.VPS_STARTING and self.ark_server_state != ArkServerState.UNKNOUN:
            self.ark_server_state = ArkServerState.ARK_STARTING
        
            # チャンネルにメッセージ送信
            sendMessage = "レンタルサーバーは起動しているので、ARKを開始します..."
            await ctx.message.channel.send(sendMessage)
            
            print("ARK Server Start.")
            
            sshCommand = "osascript /Users/user/minecraft/Git/ArkServerStart.scpt"
            subprocess.run(sshCommand, shell=True)    
            
            self.ArkConnect.start(self)
        
        else:        
            ark_server_state = ArkServerState.VPS_STARTING
        
            # チャンネルにメッセージ送信
            sendMessage = "ARKのレンタルサーバーの起動を開始します..."
            await ctx.message.channel.send(sendMessage)
            
            print("ARK ConoHa Server Start.")
        
            # サーバー起動
            startCommand = "osascript /Users/user/minecraft/Git/ConohaStart.scpt"
            subprocess.run(startCommand, shell=True)
        
            self.ConoHaStart.start(self)
        
    # ARK stopコマンド
    @commands.command()
    async def arkstop(self, ctx, stopTime = 60, isServerShut = 1):
        
        isArkServerShutdown = isServerShut
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
        
        global ark_server_state
        if ark_server_state == ArkServerState.ARK_RUNNING:
            
            ark_server_state = ArkServerState.ARK_STOPPING
            print("Ark Server Stop.")
            stopMes = str(stopTime) + "秒後にARKサーバーを停止します。"
            with MCRcon(self.conoha_server_address, str(self.ark_admin_password), int(self.ark_rcon_port))as mcr:
                mcr.command("Broadcast Stop the server after " + str(stopTime) + " seconds.")
            await ctx.message.channel.send(stopMes)
            
            time.sleep(stopTime)
            
            with MCRcon(self.conoha_server_address, str(self.ark_admin_password), int(self.ark_rcon_port))as mcr:
                mcr.command("Broadcast Stop the server.")            
            await ctx.message.channel.send("停止を開始します...")
            
            time.sleep(3)
            
            with MCRcon(self.conoha_server_address, str(self.ark_admin_password), int(self.ark_rcon_port))as mcr:
                mcr.command("DoExit")
            
            self.ArkDisConnect.start()
            
        else:
            await ctx.message.channel.send("ARKサーバーは起動していません。")
            
    # ARK commandコマンド
    @commands.command()
    async def arkcommand(self, ctx, *, cmd = "None"):   
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
        
        # コマンドが指定されてない
        if cmd == "None":        
            await ctx.message.channel.send("コマンドを入力してください。 （例） #arkcommand DoExit")
            return
            
        if self.ark_server_state == ArkServerState.ARK_RUNNING:
                   
            with MCRcon(str(self.conoha_server_address), str(self.ark_admin_password), int(self.ark_rcon_port))as mcr:
                mcr.command(str(cmd))
                
            if cmd == "DoExit":
                self.ArkDisConnect.start()
        else:
            await ctx.message.channel.send("サーバーが起動していないのでコマンドを送信出来ませんでした。")
            
    # ARK commandコマンド
    @commands.command()
    async def arksay(self, ctx, *, say = ""):   
        
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
            
        if self.ark_server_state == ArkServerState.ARK_RUNNING:
            
            with MCRcon(str(conoha_server_address), str(ark_admin_password), int(ark_rcon_port))as mcr:
                mcr.command("Broadcast " + str(say))
            
        else:
            await ctx.message.channel.send("サーバーが起動していないので発言できませんでした。")    
                
    # サーバーとの接続が行えるか（サーバーが起動しているか）指定秒おきにチェック
    @tasks.loop(seconds=5)
    async def SurveillanceServer(self):
                        
        # 接続テスト
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)

        try:
            result = mySocket.connect_ex((self.server_address, int(self.server_port)))
        except:
            return
        # 接続成功
        if result == 0:
            # 接続
            self.isServerRun = True
            
            # Botのステータス変更
            stat = discord.Game(name=self.runServerText)
            await bot.change_presence(status=DiscordPi.discord.Status.online, activity=stat)
            
            # 前回は接続できなかった場合
            if (prevConnection != result and prevConnection != 76534639315283):
                print("Server Running.")
                await self.started_channel.send("サーバーが起動しました！")
                           
            
        # 接続失敗
        else:        
            # 接続
            self.isServerRun = False
            
            # Botのステータス変更
            stat = discord.Game(name="#start でサーバーを起動できます　")
            await bot.change_presence(status=discord.Status.idle, activity=stat)
            
            # 前回は接続できていた場合
            if (self.prevConnection != result and prevConnection != 76534639315283):
                print("Server Stopped.")
                await self.started_channel.send("サーバーが停止しました。")
            
        # 今回の接続状況を保存
        self.prevConnection = result
        
        # 切断
        mySocket.close()
        
    
    # ARKサーバー（ConoHa）が立ったかチェック
    @tasks.loop(seconds=5)
    async def ConoHaStart(self):
            
        # 接続テスト（ssh）
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((self.conoha_server_address, int(self.conoha_ssh_port)))
        
        # 接続成功
        if result == 0:
        
            self.ark_server_state = ArkServerState.ARK_STARTING
            # チャンネルにメッセージ送信
            print("ARK ConoHa Server Done.")
            sendMessage = "ARKのレンタルサーバーが起動しました！\nARKを起動します..."
            await self.started_channel.send(sendMessage)
            # sshで起動
            print("ARK Server Start.")
            sshCommand = "osascript /Users/user/minecraft/Git/ArkServerStart.scpt"
            subprocess.run(sshCommand, shell=True)    
            
            self.ConoHaStart.stop()
            self.ArkConnect.start()
        
        # 切断
        mySocket.close()
        
    # ARKサーバー（ConoHa）シャットダウンチェック
    @tasks.loop(seconds=5)
    async def ConoHaStop(self):
            
        # 接続テスト（ssh）
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((self.conoha_server_address, int(self.conoha_ssh_port)))
        
        # 接続失敗
        if result != 0:
        
            self.ark_server_state = ArkServerState.VPS_SHOTDOWN
            # チャンネルにメッセージ送信
            print("ConoHa Server Shutdown　done.")
            sendMessage = "ARKのレンタルサーバーがシャットダウンしました。"
            await self.started_channel.send(sendMessage)
            
            ArkCog.ConoHaStop.stop(self)
        
        # 切断
        mySocket.close()
            
    # ARKに接続できるかチェック
    @tasks.loop(seconds=5)
    async def ArkConnect(self):
        
        # 接続テスト
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((self.conoha_server_address, int(self.ark_rcon_port)))
        
        # 接続成功
        if result == 0:
        
            self.ark_server_state = ArkServerState.ARK_RUNNING
            # チャンネルにメッセージ送信
            print("ARK Server Done.")
            sendMessage = "ARKが起動しました！（でも30秒ぐらい待ってね）"
            await self.started_channel.send(sendMessage)
            self.ArkConnect.stop(self)
        
        # 切断
        mySocket.close()
        
    # ARK切断チェック
    @tasks.loop(seconds=5)
    async def ArkDisConnect(self, isShutdown = 1):
        
        # 接続テスト
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)
        result = mySocket.connect_ex((self.conoha_server_address, int(self.ark_rcon_port)))
        
        # 接続できない
        if result != 0:
        
            # チャンネルにメッセージ送信
            print("ARK Server shutdown Done.")
            sendMessage = "ARKが終了しました。"
            
            if isArkServerShutdown != 1:          
                self.ark_server_state = ArkServerState.VPS_RUNNING  
                sendMessage += "\nレンタルサーバーのシャットダウンは行いません。"
                await self.started_channel.send(sendMessage)
                self.ArkDisConnect.stop()
                return
                
            self.ark_server_state = ArkServerState.VPS_STOPPING
            sendMessage += "\nレンタルサーバーをシャットダウンします。"
            await self.started_channel.send(sendMessage)
            
            # VM停止API
            print("ConoHa Server Shutdown.")
            sshCommand = "osascript /Users/user/minecraft/Git/ConoHaShutdown.scpt"
            subprocess.run(sshCommand, shell=True)   
            
            self.ArkDisConnect.stop()
            self.ConoHaStop.start()
        
        # 切断
        mySocket.close()

async def setup(bot):
    await bot.add_cog(ArkCog(bot))