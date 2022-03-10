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

discord = Discord(url="https://discord.com/api/webhooks/951326563423625237/nIEa1VZuzm5RIRZEXA-6Lw8jzRngbqriXd31X0WfC9lbPiuzGXAjlLZzRUyydaYmjAm8")
discord.post(content=args.arg1)