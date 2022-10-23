
import subprocess
import discord
from discord.ext import tasks, commands

class SatisfactoryCog(commands.Cog):

    isStart = False
    
    def __init__(self, bot):
        self.bot = bot

    # コマンドの大元
    @commands.group()
    async def factory(self, ctx):
        pass

    # サーバー開始
    @factory.command()
    async def start(self, ctx):
    
        # チャンネルにメッセージ送信
        sendMessage = "Satisfactoryサーバーの起動を開始します..."
        await ctx.message.channel.send(sendMessage)

        sshCommand = "osascript /Users/user/minecraft/Git/SatisfactoryStart.scpt"
        subprocess.run(sshCommand, shell=True)
        self.connect.start(ctx)

    # 接続チェッカー
    @tasks.loop(seconds=5)
    async def connect(self, ctx):
        recieve = subprocess.getoutput('echo "GAME" | nc -u 192.168.1.52 8641 -w 1')

        if (recieve == "GAME" and self.isStart == False):
            await ctx.message.channel.send("Satisfactoryサーバーが起動しました！")
            isStart = True

        elif (recieve == "" and self.isStart == True):
            await ctx.message.channel.send("Satisfactoryサーバーが停止しました。")
            isStart = False
            self.connect.stop()



async def setup(bot):
    await bot.add_cog(SatisfactoryCog(bot))