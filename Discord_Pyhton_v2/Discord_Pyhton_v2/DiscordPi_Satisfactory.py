
import subprocess
import discord
from discord.ext import tasks, commands

class SatisfactoryCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # サーバー起動
    @commands.command()
    async def factorystart(self, ctx):
    
        # 送信者がbotである場合は弾く
        if ctx.message.author.bot:
            return 
    
        # チャンネルにメッセージ送信
        sendMessage = "Satisfactoryサーバーの起動を開始します..."
        await ctx.message.channel.send(sendMessage)

        sshCommand = "osascript /Users/user/minecraft/Git/SatisfactoryStart.scpt"
        subprocess.run(sshCommand, shell=True)

async def setup(bot):
    await bot.add_cog(SatisfactoryCog(bot))