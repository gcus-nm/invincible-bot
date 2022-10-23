
import subprocess
import discord
from discord.ext import tasks, commands

class SatisfactoryCog(commands.Cog):
    
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
        self.connect.start()

    @factory.command()
    async def cnt(self, ctx):
        print("Started.")
        self.connect.start()

    # 接続チェッカー
    @tasks.loop(seconds=5)
    async def connect(self):
        recieve = subprocess.getoutput('echo "GAME" | nc -u 192.168.1.52 8641 -w 1')
        print(recieve)


async def setup(bot):
    await bot.add_cog(SatisfactoryCog(bot))