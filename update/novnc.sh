#! /bin/bash

# this installs websockify, novnc, shellinabox
# assumed already installed: apache2 and tightvncserver


echo "--> install websockify."
echo "--> ======================================="
sudo apt-get install websockify -y

# Install noVNC
# this installation will only work if :
# 1. Apache is already installed
# 2. tightvncserver is already installed

# Setup Webpage
echo "--> Setup webpage."
echo "--> ======================================="
echo " "
sudo rm -r /var/www
sudo cp -r /home/pi/si_update/sipios/www /var/
cd /var/www
sudo mkdir html
# the following line generates an error
sudo mv * html/
sudo chmod +x /var/www/html/index.php
sudo chmod +x /var/www/html/css/main.css

# Setup Shellinabox
echo "--> Setup Shellinabox."
echo "--> ======================================="
echo " "
sudo apt-get install shellinabox -y

echo "--> Setup screen."
echo "--> ======================================="
echo " "
# screen currently installed but not used. 
sudo apt-get install screen -y 

# clone noVNC
echo "--> Setup noVNC"
echo "--> ======================================="
echo " "
cd /usr/local/share
echo "--> Clone noVNC."
sudo rm -r noVNC
sudo git clone git://github.com/SigmawayLLC/noVNC
cd noVNC
sudo git pull
# change homepage
sudo cp vnc_auto.html index.html


# install systemd service

sudo wget https://raw.githubusercontent.com/SigmawayLLC/sipios/master/update/novnc.service
sudo cp novnc.service /etc/systemd/system/novnc.service
sudo chown root:root /etc/systemd/system/novnc.service
#sudo chmod +x /etc/systemd/system/novnc.service #system complains about it being marked executable. Fine, be that way.

echo "############################################################"
#sudo systemctl daemon-reload
#sudo systemctl enable novnc.service
echo "############################################################"


echo "Change bash permissions for desktop."
if grep -Fxq "xhost +" /home/pi/.bashrc
then
	#Found it, do nothing!
	echo "Found xhost in .bashrc"
else
	sudo echo "xhost +" >> /home/pi/.bashrc
fi

