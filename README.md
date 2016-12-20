# fabric-home-assistant


 ![image](images/hass_plu_fabric_logo.png)

The [Raspberry Pi All-In-One Installer](https://github.com/home-assistant/fabric-home-assistant) deploys a complete Home Assistant server including support for MQTT with websockets, Z-Wave, and the Open-Zwave Control Panel.

The only requirement is that you have a Raspberry Pi with a fresh installation of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) connected to your network.

*  Login to Raspberry Pi. For example with `ssh pi@your_raspberry_pi_ip`
*  Run the following command

```bash
$ wget -Nnv https://raw.githubusercontent.com/home-assistant/fabric-home-assistant/master/hass_rpi_installer.sh && bash hass_rpi_installer.sh
```
*Note this command is one line and not run as sudo*

Installation will take approx. 1-2 hours depending on the Raspberry Pi model the installer is being run against.

[BRUH automation](http://www.bruhautomation.com) has created [a tutorial video](https://www.youtube.com/watch?v=VGl3KTrYo6s) explaining how to install Raspbian on your Raspberry Pi and install Home Assistant using the All-In-One Installer.

Once rebooted, your Raspberry Pi will be up and running with Home Assistant. You can access it at [http://your_raspberry_pi_ip:8123](http://your_raspberry_pi_ip:8123).

The Home Assistant configuration is located at `/home/homeassistant/.homeassistant`. The virtualenv with the Home Assistant installation is located at `/srv/homeassistant/homeassistant_venv`. As part of the secure installation, a new user is added to your Raspberry Pi to run Home Assistant as named, **homeassistant**. This is a system account and does not have login or other abilities by design. When editing your configuration.yaml files, you will need to run the commands with "sudo" or by switching user.
*Windows users* - Setting up WinSCP to allow this seemlessly is detailed below.

By default, installation makes use of a Python Virtualenv. If you wish to not follow this recommendation, you may add the flag `-n` to the end of the install command specified above.

The All-In-One Installer script will do the following automatically:

*  Create all needed directories
*  Create needed service accounts
*  Install OS and Python dependencies
*  Setup a python virtualenv to run Home Assistant and components inside.
*  Run as `homeassistant` service account
*  Install Home Assistant in a virtualenv
*  Install Mosquitto, running on ports 1883 and 9001
*  Build and Install Python-openzwave in the Home Assistant virtualenv
*  Build openzwave-control-panel in `/srv/homeassistant/src/open-zwave-control-panel`
*  Build and Install libcec for the [hdmi component](https://home-assistant.io/components/hdmi_cec/)
*  Add Home Assistant to systemd services to start at boot


To upgrade the All-In-One setup:

*  Login to Raspberry Pi ```ssh pi@your_raspberry_pi_ip```
*  Change to *homeassistant* user `sudo su -s /bin/bash homeassistant`
*  Change to virtual enviroment `source /srv/homeassistant/homeassistant_venv/bin/activate`
*  Update HA `pip3 install --upgrade homeassistant`

To launch the OZWCP webapp:

*  Login to Raspberry Pi `ssh pi@your_raspberry_pi_ip`
*  Change to the ozwcp directory `cd /srv/homeassistant/src/open-zwave-control-panel/`
*  Launch the control panel `sudo ./ozwcp -p 8888`
*  Open a web browser to `http://your_pi_ip:8888`
*  Specify your zwave controller, for example `/dev/ttyACM0` and hit initialize
  
*don't check the USB box regardless of using a USB based device*


*Windows Users* - Please note that after running the installer, you will need to modify settings allowing you to "switch users" to edit your configuration files. The needed change within WinSCP is: Environment -> SCP/Shell -> Shell and set it to `sudo su -`.
