# fabric-home-assistant


 ![image](hass_icon.png) ![image](plus.png) ![image](fabric_icon.png) 
 
 Easily deploy [Home-Assistant](http://home-assistant.io) along with a websockets enabled build of [Mosquitto](https://github.com/eclipse/mosquitto) to your Raspberry Pi with Fabric. 

**What is [Fabric](http://www.fabfile.org)?**
 The official README says:
>  "Fabric is a Python (2.5-2.7) library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks."
 
 Python makes automating the build of things effortless. 
 Since I use Python3 mostly, and the offical repo's don't contain a py3 version yet, you'll need to use this version for now: [https://github.com/mathiasertl/fabric.git](https://github.com/mathiasertl/fabric)
 
###  To Run:
 
 Simply install fabric locally:
 ```pip install fabric```
 
 Clone the contents: ``` git clone https://github.com/jbags81/fabric-home-assistant.git ```
 
 Run the "deploy" function: ``` fab deploy ```
