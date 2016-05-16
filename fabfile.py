########################################
# Fabfile to:
#    - deploy supporting HA components
#    - deploy HA
########################################

# Import Fabric's API module
from fabric.api import *
import time


env.hosts = ['localhost']
env.user   = "pi"
env.password = "raspberry"


#######################
## Core server setup ##
#######################

def install_start():
    """ Notify of install start """
    print("""
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,, ,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,   ,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,     ,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,       ,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,         ,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,           ,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,             ,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,               ,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,       ,,,,.     ,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,       ,,,,,,,     ,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,       ,,,,,,,,,     ,,,     ,,,,,,,,,,
    ,,,,,,,,,,,,,,,,        ,,,   ,,,      ,,     ,,,,,,,,,,
    ,,,,,,,,,,,,,,,         ,,,   ,,,       ,     ,,,,,,,,,,
    ,,,,,,,,,,,,,,          ,,,   ,,,             ,,,,,,,,,,
    ,,,,,,,,,,,,,            ,,,,,,,              ,,,,,,,,,,
    ,,,,,,,,,,,,              ,,,,,               ,,,,,,,,,,
    ,,,,,,,,,,,                ,,,                ,,,,,,,,,,
    ,,,,,,,,,,                 ,,,                 ,,,,,,,,,
    ,,,,,,,,,        ,,,       ,,,       ,,,        ,,,,,,,,
    ,,,,,,,,       ,,,,,,,     ,,,     ,,,,,,,       ,,,,,,,
    ,,,,,,,       ,,,,,,,,,    ,,,    ,,,,,,,,,       ,,,,,,
    ,,,,,,        ,,,   ,,,    ,,,    ,,,   ,,,        ,,,,,
    ,,,,,         ,,,   ,,,    ,,,    ,,,   ,,,         ,,,,
    ,,,,,,,,,,,   ,,,   ,,,    ,,,    ,,,   ,,,   ,,,,,,,,,,
    ,,,,,,,,,,,    ,,,,,,,,    ,,,    ,,,,,,,,    ,,,,,,,,,,
    ,,,,,,,,,,,      ,,,,,,    ,,,    ,,,,,,      ,,,,,,,,,,
    ,,,,,,,,,,,        ,,,,,   ,,,   ,,,,,        ,,,,,,,,,,
    ,,,,,,,,,,,          ,,,, ,,,, ,,,,,          ,,,,,,,,,,
    ,,,,,,,,,,,           ,,,, ,,, ,,,,           ,,,,,,,,,,
    ,,,,,,,,,,,            ,,,,,,,,,,,            ,,,,,,,,,,
    ,,,,,,,,,,,             ,,,,,,,,,             ,,,,,,,,,,
    ,,,,,,,,,,,              ,,,,,,,              ,,,,,,,,,,
    ,,,,,,,,,,,               ,,,,,               ,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,                                   ,,,,,,,,,,
    ,,,,,,,,,,,   Welcome to the Home Assistant   ,,,,,,,,,,
    ,,,,,,,,,,, Raspberry Pi All-In-One Installer ,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    """)
    print("Your Raspberry Pi will reboot when the installer is complete.")
    time.sleep(3)
    print("Install is starting...")


def update_upgrade():
    """ Update OS """
    sudo("apt-get update")
    sudo("apt-get upgrade -y")


def setup_dirs():
    """ Create all needed directories and change ownership """
    with cd("/srv"):
        sudo("mkdir hass")
        sudo("chown hass hass")
        with cd("hass"):
            sudo("mkdir -p src")
            sudo("chown hass:hass src")
    with cd("/home"):
        sudo("mkdir -p hass")
        sudo("chown hass:hass hass")

def setup_users():
    """ Create service users, etc """
    sudo("useradd mosquitto")
    sudo("useradd --system hass")
    sudo("usermod -G dialout -a hass")
    sudo("usermod -d /home/hass hass")

def install_syscore():
    """ Download and install Host Dependencies. """
    sudo("aptitude install -y python3")
    sudo("aptitude install -y python3-pip")
    sudo("aptitude install -y git")
    sudo("aptitude install -y libssl-dev")
    sudo("aptitude install -y cmake")
    sudo("aptitude install -y libc-ares-dev")
    sudo("aptitude install -y uuid-dev")
    sudo("aptitude install -y daemon")
    sudo("aptitude install -y curl")
    sudo("aptitude install -y libgnutls28-dev")
    sudo("aptitude install -y libgnutlsxx28")
    sudo("aptitude install -y libgnutls-dev")
    sudo("aptitude install -y nmap")
    sudo("aptitude install -y net-tools")
    sudo("aptitude install -y sudo")
    sudo("aptitude install -y libglib2.0-dev")
    sudo("aptitude install -y cython3")
    sudo("aptitude install -y libudev-dev")
    sudo("aptitude install -y python3-sphinx")
    sudo("aptitude install -y python3-setuptools")

def install_pycore():
    """ Download and install VirtualEnv """
    sudo("pip3 install virtualenv")

def create_venv():
    """ Create home-assistant VirtualEnv """
    with cd("/srv/hass"):
            sudo("virtualenv -p python3 hass_venv", user="hass")


#######################################################
## Build and Install Applications without VirtualEnv ##
#######################################################

def setup_homeassistant_novenv():
    """ Install Home-Assistant """
    sudo("pip3 install homeassistant", user="hass")

def setup_openzwave_novenv():
    """ Install python-openzwave """
    sudo("pip3 install --upgrade cython", user="hass")
    with cd("/srv/hass/src"):
        sudo("git clone https://github.com/OpenZWave/python-openzwave.git", user="hass")
        with cd("python-openzwave"):
            sudo("git checkout python3", user="hass")
            sudo("make build", user="hass")
            sudo("make install", user="hass")

def setup_services_novenv():
    """ Enable applications to start at boot via systemd """
    with cd("/etc/systemd/system/"):
        put("mosquitto.service", "mosquitto.service", use_sudo=True)
        put("home-assistant_novenv.service", "home-assistant_novenv.service", use_sudo=True)

    sudo("systemctl enable mosquitto.service")
    sudo("systemctl enable home-assistant_novenv.service")
    sudo("systemctl daemon-reload")


def setup_motd():
    """ Configures HASS MOTD Banner """
    with cd("/etc/ssh"):
        put("sshd_config", "sshd_config", use_sudo=True)

    with cd("/etc/profile.d"):
        put("motd.sh", "motd.sh", use_sudo=True)
        sudo("chmod +x motd.sh")
        sudo("chown root:root motd.sh")




####################################
## Build and Install Applications ##
####################################

def setup_mosquitto():
    """ Build and Install Mosquitto """
    with cd("/tmp"):
        sudo("curl -O https://libwebsockets.org/git/libwebsockets/snapshot/libwebsockets-1.4-chrome43-firefox-36.tar.gz")
        sudo("tar xvf libwebsockets*")
        with cd("libwebsockets*"):
            sudo("mkdir build")
            with cd("build"):
                sudo("cmake ..")
                sudo("make install")
                sudo("ldconfig")
                with cd("/srv/hass/src"):
                    sudo("wget http://mosquitto.org/files/source/mosquitto-1.4.4.tar.gz")
                    sudo("tar zxvf mosquitto-1.4.4.tar.gz")
                    with cd("mosquitto-1.4.4"):
                        sudo("sed -i 's/WITH_WEBSOCKETS:=no.*/WITH_WEBSOCKETS:=yes/' /srv/hass/src/mosquitto-1.4.4/config.mk")
                        sudo("make")
                        sudo("make install")
                        with cd("/etc/mosquitto"):
                            put("mosquitto.conf", "mosquitto.conf", use_sudo=True)

def setup_homeassistant():
    """ Activate Virtualenv, Install Home-Assistant """
    sudo("source /srv/hass/hass_venv/bin/activate && pip3 install homeassistant", user="hass")

def setup_openzwave():
    """ Activate Virtualenv, Install python-openzwave"""
    sudo("source /srv/hass/hass_venv/bin/activate && pip3 install --upgrade cython", user="hass")
    with cd("/srv/hass/src"):
        sudo("git clone https://github.com/OpenZWave/python-openzwave.git", user="hass")
        with cd("python-openzwave"):
            sudo("git checkout python3", user="hass")
            sudo("source /srv/hass/hass_venv/bin/activate && make build", user="hass")
            sudo("source /srv/hass/hass_venv/bin/activate && make install", user="hass")


def setup_libmicrohttpd():
    """ Build and install libmicrohttpd """
    with cd("/srv/hass/src"):
        sudo("mkdir libmicrohttpd")
        sudo("chown hass:hass libmicrohttpd")
        sudo("wget ftp://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.19.tar.gz", user="hass")
        sudo("tar zxvf libmicrohttpd-0.9.19.tar.gz")
        with cd("libmicrohttpd-0.9.19"):
            sudo("./configure")
            sudo("make")
            sudo("make install")

def setup_openzwave_controlpanel():
    """ Build and Install open-zwave-control-panel """
    with cd("/srv/hass/src"):
        sudo("git clone https://github.com/OpenZWave/open-zwave-control-panel.git", user="hass")
        with cd("open-zwave-control-panel"):
            put("Makefile", "Makefile", use_sudo=True)
            sudo("make")
            sudo("ln -sd /srv/hass/hass_venv/lib/python3.4/site-packages/libopenzwave-0.3.0-py3.4-linux-armv7l.egg/config")
        sudo("chown -R hass:hass /srv/hass/src/open-zwave-control-panel")

def setup_services():
    """ Enable applications to start at boot via systemd """
    with cd("/etc/systemd/system/"):
        put("mosquitto.service", "mosquitto.service", use_sudo=True)
        put("home-assistant.service", "home-assistant.service", use_sudo=True)
    sudo("systemctl enable mosquitto.service")
    sudo("systemctl enable home-assistant.service")
    sudo("systemctl daemon-reload")

def setup_motd():
    """ Configures HASS MOTD Banner """
    with cd("/etc/ssh"):
        put("sshd_config", "sshd_config", use_sudo=True)

    with cd("/etc/profile.d"):
        put("motd.sh", "motd.sh", use_sudo=True)
        sudo("chmod +x motd.sh")
        sudo("chown root:root motd.sh")

#############
## Deploy! ##
#############

def deploy():

    ## Install Start ##
    install_start()

    ## Initial Update and Upgrade ##
    update_upgrade()

    ## Setup service accounts ##
    setup_users()

    ## Setup directories ##
    setup_dirs()

    ## Install dependencies ##
    install_syscore()
    install_pycore()

    ## Create VirtualEnv ##
    create_venv()

    ## Build and Install Mosquitto ##
    setup_mosquitto()

    ## Activate venv, install Home-Assistant ##
    setup_homeassistant()

    ## Activate venv, build and install python-openzwave ##
    setup_openzwave()

    ## Build and install libmicrohttpd ##
    setup_libmicrohttpd()

    ## Build and install open-zwave-control-panel ##
    setup_openzwave_controlpanel()

    ## Make apps start at boot ##
    setup_services()

    ## Setup MOTD Banner ##
    setup_motd()

    ## Reboot the system ##
    reboot()




def deploy_novenv():

    ## Install Start ##
    install_start()

    ## Initial Update and Upgrade ##
    update_upgrade()

    ## Setup service accounts ##
    setup_users()

    ## Setup directories ##
    setup_dirs()

    ## Install dependencies ##
    install_syscore()

    ## Build and Install Mosquitto ##
    setup_mosquitto()

    ## Activate venv, install Home-Assistant ##
    setup_homeassistant_novenv()

    ## Activate venv, build and install python-openzwave ##
    setup_openzwave_novenv()

    ## Build and install libmicrohttpd ##
    setup_libmicrohttpd()

    ## Build and install open-zwave-control-panel ##
    setup_openzwave_controlpanel()

    ## Make apps start at boot ##
    setup_services_novenv()

    ## Setup MOTD Banner ##
    setup_motd()

    ## Reboot the system ##
    reboot()
