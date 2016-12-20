#!/usr/bin/env bash
# Home Assistant Raspberry Pi Installer Kickstarter
# Copyright (C) 2016 Jonathan Baginski - All Rights Reserved
# Permission to copy and modify is granted under the MIT License
# Last revised 5/15/2016

## Run pre-install apt package dependency checks ##

while getopts ":n" opt; do
  case $opt in
    n)

    me=$(whoami)

    sudo apt-get update

    PKG_PYDEV=$(dpkg-query -W --showformat='${Status}\n' python3-dev|grep "install ok installed")
    echo Checking for python3-dev: $PKG_PYDEV
    if [ "" == "$PKG_PYDEV" ]; then
      echo "No python3-dev. Setting up python3-dev."
      sudo apt-get --force-yes --yes install python3-dev
    fi

    PKG_PYPIP=$(dpkg-query -W --showformat='${Status}\n' python3-pip|grep "install ok installed")
    echo Checking for python3-pip: $PKG_PYPIP
    if [ "" == "$PKG_PYPIP" ]; then
      echo "No python3-pip. Setting up python3-pip."
      sudo apt-get --force-yes --yes install python3-pip
    fi

    PKG_GIT=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
    echo Checking for python3-pip: $PKG_GIT
    if [ "" == "$PKG_GIT" ]; then
      echo "No git. Setting up git."
      sudo apt-get --force-yes --yes install git
    fi

    sudo /usr/bin/pip3 install pycrypto
    sudo /usr/bin/pip3 install fabric3

    git clone https://github.com/home-assistant/fabric-home-assistant.git

    ( cd /home/$me/fabric-home-assistant && fab deploy_novenv -H localhost 2>&1 | tee installation_report.txt )
    exit
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

me=$(whoami)

sudo apt-get update

PKG_PYDEV=$(dpkg-query -W --showformat='${Status}\n' python3-dev|grep "install ok installed")
echo Checking for python3-dev: $PKG_PYDEV
if [ "" == "$PKG_PYDEV" ]; then
  echo "No python3-dev. Setting up python3-dev."
  sudo apt-get --force-yes --yes install python3-dev
fi

PKG_PYPIP=$(dpkg-query -W --showformat='${Status}\n' python3-pip|grep "install ok installed")
echo Checking for python3-pip: $PKG_PYPIP
if [ "" == "$PKG_PYPIP" ]; then
  echo "No python3-pip. Setting up python3-pip."
  sudo apt-get --force-yes --yes install python3-pip
fi

PKG_GIT=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
echo Checking for python-pip: $PKG_GIT
if [ "" == "$PKG_GIT" ]; then
  echo "No git. Setting up git."
  sudo apt-get --force-yes --yes install git
fi

sudo /usr/bin/pip3 install pycrypto
sudo /usr/bin/pip3 install fabric3

git clone https://github.com/home-assistant/fabric-home-assistant.git


( cd /home/$me/fabric-home-assistant && fab deploy -H localhost 2>&1 | tee installation_report.txt )
exit
