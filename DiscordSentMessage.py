# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

from discordwebhook import Discord
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('arg1')
args = parser.parse_args()

discord = Discord(url="https://discord.com/api/webhooks/951316286237995048/im70FXVqHWLwwxGp7pOC3zG9PxFX6-VJZdNahOsew2aKronNkIH5YVrHe5Go5Gt-ejXM")
discord.post(content=args.arg1)