#! /bin/bash

ram=$1
version=$2
javaVer=$3

# show build server info
echo -------------------------------
echo Build server info
echo
echo -e "Version\t =" $version
echo -e "RAM\t =" $ram "GB"
echo -------------------------------

# Java version
javaPath="java"

if [ $javaVer -eq 17 ] ; then
  javaPath="/usr/bin/java"
elif [ $javaVer -eq 8 ] ; then
  javaPath="java"
fi


# Build
cd /User/user/minecraft/servers/${version}
sudo nice -n -15 $javaPath -Xms${ram}G -Xmx${ram}G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -XX:G1NewSizePercent=40 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:InitiatingHeapOccupancyPercent=20 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui

# Backup To Google Drive
echo
echo "Starting Backup To Google Drive. "
echo
cd /home/pi/minecraft/servers
rclone sync -P $version GoogleDrive:RaspberryPi/Minecraft/$version

echo
read -p "Exit to press Enter."
cd
