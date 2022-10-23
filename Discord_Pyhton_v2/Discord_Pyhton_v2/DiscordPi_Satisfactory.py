
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


async def setup(bot):
    await bot.add_cog(SatisfactoryCog(bot))