# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:48:56 2022

@author: gcus_nm12
"""

import os
import discord.ext
from discord.ext import commands

client = commands.Bot(command_prefix='!')

# ここにコードを書く

client.run(os.environ.get('DISCORD_TOKEN'))