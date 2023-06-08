# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:52:13 2022

@author: gcus_nm12
"""

import subprocess
import socket
import discord
from discord.ext import tasks, commands
from mcrcon import MCRcon

class MinecraftCog(commands.Cog):

    # 起動中テキスト
    runServerText = "Minecraft Server"

    # アドレス
    server_address = 'gcus-MacPro.local'
    # マイクラポート
    server_port = 25024
    # rconパスワード
    rcon_password = 2126
    # rconポート
    rcon_port = 25025

    runServerText = ""

    isServerRun = False

    server_wait_time = 60

    prevConnection = 76534639315283
    
    def __init__(self, bot):
        self.bot = bot

    # commandコマンド
    @commands.command()
    async def command(self, ctx, *, cmd = "None"):   
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
    
        # コマンドが指定されてない
        if cmd == "None":        
            await ctx.message.channel.send("コマンドを入力してください。 （例） #command list")
            return
    
        if self.isServerRun:    
            # サーバーアドレス
            global server_address
            # rconパスワード
            global rcon_password
            # rconポート
            global rcon_port       
        
            with MCRcon(str(server_address), str(rcon_password), int(rcon_port))as mcr:
                res = mcr.command(str(cmd))
        
            await ctx.message.channel.send(res)
        
        else:
            await ctx.message.channel.send("サーバーが起動していないのでコマンドを送信出来ませんでした。")    

    # startコマンド
    @commands.command()
    async def start(self, ctx, version = "1.20.0", ram = 12):
    
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
    
        global isServerStartRequest
    
        if self.isServerRun:
            await ctx.message.channel.send("既にサーバーが起動しているため、起動できません。")
            return
    
        # javaバージョン
        javaVer = "17"
    
        # サーバーバージョンメッセージ
        versionMessage = version
    
        # 起動鯖のバージョン指定
        if  (version == "1.18.1" or version == "1.18.1P"):
        
            version = "1.18.1P"
            versionMessage = "1.18.1 バニラサーバー"
            self.runServerText = "1.18.1 バニラサーバー "
            javaVer = "17"
        
        elif (version == "1.12.2Mohist" or version == "takumi" or
            version == "Takumi" or version == "TAKUMI"):
        
            version = "1.12.2Mohist"
            versionMessage = "1.12.2 匠サーバー"
            self.runServerText = "1.12.2 匠サーバー "
            javaVer = "8"
        
        elif (version == "1.12.2SkyFactory4" or
              version == "sky" or version == "Sky" or 
              version == "skyfactory" or version == "SkyFactory"):
                
            version = "1.12.2SkyFactory4"
            versionMessage = "1.12.2 SkyFactory 4"
            self.runServerText = "1.12.2 SkyFactory 4 "
            javaVer = "8"

        elif (version == "1.19"):
            version = "1.19"
            versionMessage = "1.19"
            self.runServerText = "1.19"
            javaVer = "17"

        elif (version == "1.19.3"):
            version = "1.19.3"
            versionMessage = "1.19.3"
            self.runServerText = "1.19.3"
            javaVer = "17" 
            
        elif (version == "1.20.0"):
            version = "1.20.0"
            versionMessage = "1.20.0"
            self.runServerText = "1.20.0"
            javaVer = "17"

        elif (version == "1"):
            version = "1.12.2Kumada"
            versionMessage = "1.12.2"
            self.runServerText = "1.12.2"
            javaVer = "8"
    
        # チャンネルにメッセージ送信
        sendMessage = versionMessage + " の起動を開始します..."
        await ctx.message.channel.send(sendMessage)
    
        # 起動コマンドをシェルで起動
        print("Minecraft Server Start.")
        command = "osascript /Users/user/minecraft/Git/BuildMac.scpt";
        command = command + " " + str(version) + " " + str(ram) + " " + str(javaVer)

        self.SurveillanceServer.start()
    
        subprocess.run(command, shell=True)
    
    # stopコマンド
    @commands.command()
    async def stop(self, ctx):
    
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
    
        if self.isServerRun:
            print("Minecraft Server Stop.")
            await ctx.message.channel.send("サーバーを停止します...")
            # サーバーアドレス
            global server_address
            # rconパスワード
            global rcon_password
            # rconポート
            global rcon_port
        
            with MCRcon(str(server_address), str(rcon_password), int(rcon_port))as mcr:
                mcr.command("stop")
            
        else:
            await ctx.message.channel.send("サーバーは起動していません。")


    # サーバーとの接続が行えるか（サーバーが起動しているか）指定秒おきにチェック
    @tasks.loop(seconds=5)
    async def SurveillanceServer(self):
                    
        # 接続テスト
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(5)

        try:
            result = mySocket.connect_ex((self.server_address, int(self.server_port)))
        except:
            print("error connection")
            return

        # 接続成功
        if result == 0:
            # 接続
            self.isServerRun = True
        
            # Botのステータス変更
            stat = discord.Game(name=self.runServerText)
            await self.bot.change_presence(status=DiscordPi.discord.Status.online, activity=stat)
        
            # 前回は接続できなかった場合
            if (self.prevConnection != result and self.prevConnection != 76534639315283):
                print("Server Running.")
                await self.started_channel.send("サーバーが起動しました！")
                       
        
        # 接続失敗
        else:        
            # 接続
            self.isServerRun = False
        
            # 前回は接続できていた場合
            if (self.prevConnection != result and self.prevConnection != 76534639315283):
                print("Server Stopped.")
                await self.started_channel.send("サーバーが停止しました。")
        
        # 今回の接続状況を保存
        self.prevConnection = result
    
        # 切断
        mySocket.close()

    async def setup(bot):
        await bot.add_cog(MinecraftCog(bot))