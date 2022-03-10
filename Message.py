# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import discord.ext
import random
from discord.ext import commands
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('arg1')
args = parser.parse_args()

channel_id_server = 852963766630613032

client = commands.Bot(command_prefix='!')
channel = client.get_channel(channel_id_server)

@client.command()
async def dice(ctx, arg = 6):
  dice_limit = int(arg)
  await ctx.send(random.randrange(dice_limit) + 1)

@client.event
async def on_ready():
  await channel.send("サーバーが起動しました！")

client.run(os.environ.get('DISCORD_TOKEN'))