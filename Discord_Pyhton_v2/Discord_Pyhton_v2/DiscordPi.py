# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import subprocess
import discord
import os
from discord.ext import tasks, commands

from DiscordPi_ARK import ArkCog
from DiscordPi_Minecraft import MinecraftCog
from DiscordPi_Satisfactory import SatisfactoryCog

intents = discord.Intents.all()
client = commands.Bot(command_prefix='#', intents=intents)

# Python（Bot）起動時
@client.event
async def on_ready():

    await client.add_cog(MinecraftCog(client))
    await client.add_cog(ArkCog(client))
    await client.add_cog(SatisfactoryCog(client))

    print("Bot Start.")
    
# rebootコマンド
@client.command()
async def reboot(ctx):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 

    print("Reboot.")
    await ctx.message.channel.send("サーバーPCの再起動を行います。")
    
    # リブート
    subprocess.run("sudo reboot", shell=True)

client.load_extension('DiscordPi_Minecraft')
client.load_extension('DiscordPi_ARK')
client.load_extension('DiscordPi_Satisfactory')

client.run(os.environ.get('DISCORD_TOKEN'))