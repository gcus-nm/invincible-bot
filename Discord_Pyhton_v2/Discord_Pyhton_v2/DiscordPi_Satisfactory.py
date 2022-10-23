
import subprocess
import discord
from discord.ext import tasks, commands
from enum import IntEnum

class SatisfactoryCog(commands.Cog):

    class FactoryServerState(IntEnum):
        SHUTDOWN = 0    # 停止中
        STARTING = 1    # 起動中
        RUNNING  = 2    # 実行中

    state = FactoryServerState.SHUTDOWN
    
    def __init__(self, bot):
        self.bot = bot

    # サーバー疎通確認（UDP）
    def is_server_connected(self):        
        recieve = subprocess.getoutput('echo "GAME" | nc -u 192.168.1.52 8641 -w 1')
        return recieve != ''

    # コマンドの大元
    @commands.group()
    async def factory(self, ctx):
        if (self.is_server_connected()):
            self.state = self.FactoryServerState.RUNNING
        else:
            self.state = self.FactoryServerState.SHUTDOWN

    # サーバー開始
    @factory.command()
    async def start(self, ctx):

        if (self.state >= self.FactoryServerState.STARTING):            
            sendMessage = "Satisfactoryサーバーはすでに起動しています。"
            await ctx.message.channel.send(sendMessage)
            return
    
        try:
            # チャンネルにメッセージ送信
            sendMessage = "Satisfactoryサーバーの起動を開始します..."
            await ctx.message.channel.send(sendMessage)
            self.state = self.FactoryServerState.STARTING

            sshCommand = "osascript /Users/user/minecraft/Git/SatisfactoryStart.scpt"
            subprocess.run(sshCommand, shell=True)
            self.connect.start(ctx)

        except exception as e:
            sendMessage = "Satisfactoryサーバーを起動できませんでした。"
            print(e)
            await ctx.message.channel.send(sendMessage)
            self.state = self.FactoryServerState.SHUTDOWN

    # 接続チェッカー
    @tasks.loop(seconds=5)
    async def connect(self, ctx):
        connect = self.is_server_connected()

        if (connect == True and self.state != self.FactoryServerState.RUNNING):
            await ctx.message.channel.send("Satisfactoryサーバーが起動しました！")
            self.state = self.FactoryServerState.RUNNING

        elif (connect == False and self.state == self.FactoryServerState.RUNNING):
            await ctx.message.channel.send("Satisfactoryサーバーが停止しました。")
            self.state = self.FactoryServerState.SHUTDOWN            
            sshCommand = "sshpass -p Smashsmash12 ssh gcus_nm12@192.168.1.52 -p 22 taskkill -im UE4Server-Win64-Shipping.exe /F"
            subprocess.run(sshCommand, shell=True)
            self.connect.stop()


async def setup(bot):
    await bot.add_cog(SatisfactoryCog(bot))