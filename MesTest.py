# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:18:52 2022

@author: gcus_nm12
"""

from discordwebhook import discord

discord = discord(url="https://discord.com/api/webhooks/951316286237995048/im70FXVqHWLwwxGp7pOC3zG9PxFX6-VJZdNahOsew2aKronNkIH5YVrHe5Go5Gt-ejXM")
discord.post(content="メッセージテスト")