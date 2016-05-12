########################################
# Fabfile to:
#    - deploy supporting HA components
#    - deploy HA
########################################

# Import Fabric's API module
from fabric.api import *


env.hosts = [
    'host.example.com',
  # 'ip.add.rr.ess
  # 'server2.domain.tld',
]
# Set the username
env.user   = "pi"

# Set the password [NOT RECOMMENDED]
env.password = "raspberry"


#######################
## Core server setup ##
#######################

def update_upgrade():
    """ Update OS """
    sudo("apt-get update")
    sudo("apt-get upgrade -y")


def setup_dirs():
    """ Create all needed directories """
    with cd("/home/pi/"):
        run("mkdir -p src")
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
    """ Download and install python3. """
    sudo("aptitude install -y python3")
    sudo("aptitude install -y python3-pip")
    sudo("aptitude install -y git")
    sudo("aptitude install -y libssl-dev")
    sudo("aptitude install -y cmake")
    sudo("aptitude install -y libc-ares-dev")
    sudo("aptitude install -y uuid-dev")
    sudo("aptitude install -y daemon")
    sudo("aptitude install -y curl")

def install_pycore():
    """ Download and install VirtualEnv """
    sudo("pip3 install virtualenv")

def create_venv():
    """ Create home-assistant VirtualEnv """
    with cd("/srv/hass"):
            sudo("virtualenv -p python3 hass_venv", user="hass")


####################################
## Build and Install Applications ##
####################################

def setup_mosquitto():
    """ Build and Install Mosquitto """
    with cd("/tmp"):
        run("curl -O https://libwebsockets.org/git/libwebsockets/snapshot/libwebsockets-1.4-chrome43-firefox-36.tar.gz")
        run("tar xvf libwebsockets*")
        with cd("libwebsockets*"):
            run("mkdir build")
            with cd("build"):
                run("cmake ..")
                sudo("make install")
                sudo("ldconfig")
                with cd("/home/pi/src"):
                    run("wget http://mosquitto.org/files/source/mosquitto-1.4.4.tar.gz")
                    run("tar zxvf mosquitto-1.4.4.tar.gz")
                    with cd("mosquitto-1.4.4"):
                        run("sed -i 's/WITH_WEBSOCKETS:=no.*/WITH_WEBSOCKETS:=yes/' ~/src/mosquitto-1.4.4/config.mk")
                        run("make")
                        sudo("make install")
                        with cd("/etc/mosquitto"):
                            put("mosquitto.conf", "mosquitto.conf", use_sudo=True)

def setup_homeassistant():
    """ Activate VirtualEnv, Install Home-Assistant """
    sudo("source /srv/hass/hass_venv/bin/activate && pip3 install homeassistant", user="hass")

def setup_pyzwave():
    """ Install python-openzwave and configure """
    sudo("apt-get install -y cython3 libudev-dev python3-sphinx python3-setuptools")
    sudo("source /srv/hass/hass_venv/bin/activate && pip3 install --upgrade cython", user="hass")
    with cd("/srv/hass/src"):
        sudo("git clone https://github.com/OpenZWave/python-openzwave.git", user="hass")
        with cd("python-openzwave"):
            sudo("git checkout python3", user="hass")
            sudo("source /srv/hass/hass_venv/bin/activate && PYTHON_EXEC=`which python3` make build", user="hass")
            sudo("source /srv/hass/hass_venv/bin/activate && PYTHON_EXEC=`which python3` make install", user="hass")

def setup_services():
    """ Enable applications to start at boot via systemd """
    with cd("/etc/systemd/system/"):
        put("mosquitto.service", "mosquitto.service", use_sudo=True)
        put("home-assistant.service", "home-assistant.service", use_sudo=True)
    sudo("systemctl enable mosquitto.service")
    sudo("systemctl enable home-assistant.service")
    sudo("systemctl daemon-reload")

#############
## Deploy! ##
#############

def deploy():

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
    setup_pyzwave()

    ## Make apps start at boot ##
    setup_services()
