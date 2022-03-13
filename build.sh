#! /bin/bash

version=$1
ram=$2
javaVer=$3

# set CPU frequency max
sudo cpufreq-set -g performance

# Build
lxterminal -e bash /home/pi/minecraft/Git/buildChild.sh $ram $version $javaVer
