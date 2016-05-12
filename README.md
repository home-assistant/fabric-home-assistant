# fabric-home-assistant


 ![image](images/hass_icon.png) ![image](images/plus.png) ![image](images/fabric_icon.png) 
 
 Easily deploy [Home-Assistant](http://home-assistant.io) and it's components from a fresh Raspbian Jessie/Jessie-Lite or Debian 8 install.  The ```fab deploy``` script will do the following:
*  Create needed directories
*  Create needed service accounts
*  Install OS and Python dependencies
*  Setup a virtualenv to run Home-Assistant and components inside.
*  Run as a service account
*  Build Mosquitto from source with websocket support
*  Install Python-openzwave in the Home-Assistant virtualenv
*  Add both Home-Assistant and Mosquitto to systemd services



**What is [Fabric](http://www.fabfile.org)?**
 The official README says:
>  "Fabric is a Python (2.5-2.7) library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks."
 
 Python makes automating the build of things effortless. 
 Since I use Python3 mostly, and the offical repo's don't contain a py3 version yet, you'll need to use this version for now: [https://github.com/mathiasertl/fabric.git](https://github.com/mathiasertl/fabric)
 
###  Usage:
 
 Simply install fabric locally:
 ```pip install fabric``` (for python 3 support, install fabric3 [https://github.com/mathiasertl/fabric.git](https://github.com/mathiasertl/fabric))
 
 Ensure you're able to SSH into the target server. 
 
 Clone the contents: ``` git clone https://github.com/jbags81/fabric-home-assistant.git ```
 Add the host info from before to the beginning of ```fabfile.py```
 
 Run the "deploy" function to build a new home-assistant server: ``` fab deploy ``` then reboot. Everything will start at boot, and Home-Assistant is accessible from **http://your_server_ip:8123**
 
 Fabric allows any of the underlying functions to be ran individually as well. run ``` fab -l ``` to see a list of all callable jobs. 
 
 Future support for non-virtualenv based servers will be added, along with the ability to auto upload existing or backup .yaml Home-Assistant configs. I'm also working on a turn-key devlopment script to make testing and development environments one click setups.. More to come!
 
 
 
 
**Tested with Raspbian Jessie, Jessie-Lite, and Debian 8**
