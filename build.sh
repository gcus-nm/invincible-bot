#! /bin/bash

version=$1
ram=$2
javaVer=$3

# Build
/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal bash /User/user/minecraft/Git/buildChild.sh $ram $version $javaVer
