# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:48:56 2022

@author: gcus_nm12
"""

import discord

client = discord.cliant()

#鯖チャンネルのID
CHANNEL_ID_SERVER = 852963766630613032

async def ServerOn():
    channel = client.get_channel(CHANNEL_ID_SERVER)
    await channel.send('サーバーが起動しました')
    
async def ServerOff():
    channel = client.get_channel(CHANNEL_ID_SERVER)
    await channel.send('サーバーが停止しました')
    

client.run(('DISCORD_TOKEN'))