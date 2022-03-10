# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import discord
import argphase

parser = argphase.ArgumentParser()
parser.add_argument('arg1')
args = parser.parse_args()

channel_id_server = 852963766630613032

cliant = discord.Cliant()
channel = cliant.get_channel(channel_id_server)

if args.arg1 == 1:
    channel.send("test")

cliant.run(os.environ.get('DISCORD_TOKEN'))