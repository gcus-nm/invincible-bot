#! /bin/bash

botPath=/opt/Git/DiscordPi.py

echo "start Discordbot."

python -m pip install -U discord.py
python $botPath

read -p "YEAH"

