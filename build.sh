#! /bin/bash

version=1.18.1P
ram=6

# show build server info
echo -------------------------------
echo Build server info
echo
echo -e "Version\t =" $version
echo -e "RAM\t =" $ram "GB"
echo -------------------------------

# set CPU frequency max
sudo cpufreq-set -g performance

# Build
bash buildChild.sh $ram $version