#! /bin/bash

version=1.18.1P
ram=6

# set CPU frequency max
sudo cpufreq-set -g performance

# Build
lxterminal -e bash /home/pi/minecraft/Git/buildChild.sh $ram $version
