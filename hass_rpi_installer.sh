#!/usr/bin/env bash
# Home Assistant Raspberry Pi Installer Kickstarter
# Copyright (C) 2016 Jonathan Baginski - All Rights Reserved
# Permission to copy and modify is granted under the MIT License
# Last revised 5/15/2016

## Run pre-install apt package dependency checks ##
PKG_PYDEV=$(dpkg-query -W --showformat='${Status}\n' python-dev|grep "install ok installed")
echo Checking for python-dev: $PKG_PYDEV
if [ "" == "$PKG_PYDEV" ]; then
  echo "No python-dev. Setting up python-dev."
  sudo apt-get --force-yes --yes install python-dev
fi

PKG_PYPIP=$(dpkg-query -W --showformat='${Status}\n' python-pip|grep "install ok installed")
echo Checking for python-pip: $PKG_PYPIP
if [ "" == "$PKG_PYPIP" ]; then
  echo "No python-pip. Setting up python-pip."
  sudo apt-get --force-yes --yes install python-pip
fi

PKG_GIT=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
echo Checking for python-pip: $PKG_GIT
if [ "" == "$PKG_GIT" ]; then
  echo "No git. Setting up git."
  sudo apt-get --force-yes --yes install git
fi

git clone https://github.com/jbags81/fabric-home-assistant.git

## Ready to go, kick off installer script ##
/home/pi/fabric-home-assistant/python rpi_installer.py
