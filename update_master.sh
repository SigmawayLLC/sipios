#! /bin/bash
# This is the master script for updating Raspbian for Robots.
# All updates should be run from this script.
# This script should RARELY be changed.

##############################################################################################################
# 0.    Check for internet connection.
echo " "
echo "Check for internet connectivity..."
echo "=================================="

wget -q --tries=2 --timeout=100 --output-document=/dev/null http://raspberrypi.org
if [ $? -eq 0 ];then
	echo "Connected.  Do not close this window!"
	sleep 1
else
	echo "Unable to Connect, try again !!!"
	echo "Connect your Pi to the internet and try again."
	echo "This window will close in 10 seconds."
	sleep 10
	exit 0
fi
curl --silent https://raw.githubusercontent.com/SigmawayLLC/script_tools/master/install_script_tools.sh | bash

PIHOME=/home/pi
SGMW=Sgmw
SGMW_PATH=$PIHOME/$SGMW
SGMW_LIB=lib
SGMW_LIB_PATH=$SGMW_PATH/$SGMW_LIB
SGMW_SCRIPT_TOOLS=$SGMW/script_tools
SGMW_SCRIPT_TOOLS_PATH=$SGMW_LIB_PATH/$SGMW_SCRIPT_TOOLS

source $SGMW_SCRIPT_TOOLS_PATH/functions_library.sh
##############################################################################################################
# 1.    Update the Source Files.  Pull the Sipi for robots Github repo and put it in a subdirectory of pi.
#		Get the latest update information.

# If the directory exists, delete it.

if [ -d /home/pi/si_update ] ; then
	sudo rm -r /home/pi/si_update
fi

# Make the directory again.  Clone into it.  
mkdir /home/pi/si_update
cd /home/pi/si_update
sudo git clone https://github.com/SigmawayLLC/sipios/
cd sipios
cd /home/pi/si_update/sipios/



# Make files executable.
echo "MAKE FILES EXECUTABLE."
echo "=============================="
sudo chmod +x /home/pi/si_update/sipios/update_master.sh
sudo chmod +x /home/pi/si_update/sipios/upd_script/update_all.sh

##############################################################################################################
# 2.	Change all desktop icons around.
#
echo "START DESKTOP SHORTCUT UPDATE."
echo "=============================="
# Update the Desktop Shortcut for Software Update
sudo chmod +x /home/pi/si_update/sipios/desktop_shortcut_update.sh
sudo chmod +x /home/pi/si_update/sipios/desktop_shortcut_update_start.sh
delete_file /home/pi/Desktop/desktop_shortcut_update.desktop
sudo cp /home/pi/si_update/sipios/desktop_shortcut_update.desktop /home/pi/Desktop
sudo chmod +x /home/pi/Desktop/desktop_shortcut_update.desktop

delete_file /home/pi/Desktop/shutdown.desktop
sudo cp /home/pi/si_update/sipios/shutdown.desktop /home/pi/Desktop
sudo chmod +x /home/pi/Desktop/shutdown.desktop

delete_file /home/pi/Desktop/dexterindustries.desktop

delete_file /home/pi/Desktop/idle3.desktop
delete_file /home/pi/Desktop/idle.desktop
delete_file /home/pi/Desktop/gksu.desktop

# Rename the wifi control.  Change the icon.
delete_file /home/pi/Desktop/wpa_gui.desktop
sudo cp /home/pi/si_update/sipios/desktop/wpa_gui.desktop /home/pi/Desktop
sudo chmod +x /home/pi/Desktop/wpa_gui.desktop

# Update the Backup
delete_file /home/pi/Desktop/backup.desktop
sudo cp /home/pi/si_update/sipios/backup/backup.desktop /home/pi/Desktop
sudo chmod +x /home/pi/Desktop/backup.desktop

# Update the Desktop Shortcut for GrovePi and GoPiGo Firmware Update
# sudo chmod +x /home/pi/di_update/Raspbian_For_Robots/desktop_firmware_update.sh
# sudo sh /home/pi/di_update/Raspbian_For_Robots/desktop_firmware_update.sh

##############################################################################################################
# 3.    Execute the file update_all.sh
# Make sure we keep a log file.

# ensure we have wx version 2.8 and not version 3.0
sudo apt-get install python-wxgtk2.8 -y
sudo apt-get purge python-wxgtk3.0 -y

# Run update_all.sh
NOW=$(date +%m-%d-%Y-%H%M%S)
LOG_FILE="/home/pi/si_update/log_output.$NOW.txt"

# Start sipi_for_robots_update.py
# This is the GUI that will let you choose to: 
# 	1. OS Update
#	2. DI Software Update
#	3. DI Hardware Update

echo "START UPDATE GUI."
echo "=============================="
today=`date '+%Y_%m_%d__%H_%M_%S'`;
filename="/home/pi/Desktop/Sipi_Software_Update_log_$today.txt" 
script -c 'sudo python /home/pi/si_update/sipios/raspbian_for_robots_update.py 2>&1' -f $filename
delete_file /home/pi/index.html*

###
# Old Code John's holding onto as backup.
# sudo /home/pi/di_update/Raspbian_For_Robots/upd_script/update_all.sh 2>&1 | tee ${LOG_FILE}
# sudo /home/pi/di_update/Raspbian_For_Robots/upd_script/update_all.sh

# All output and errors should go to a local file.


##############################################################################################################
# 4.    Reboot the Pi.
#               We must reboot for folks.
echo "To finish any changes, we need to reboot the Pi."
echo "Pi must reboot for changes and updates to take effect."
# echo "Rebooting in 5 seconds!"
# sleep 1
# echo "Rebooting in 4 seconds!"
# sleep 1
# echo "Rebooting in 3 seconds!"
# sleep 1
# echo "Rebooting in 2 seconds!"
# sleep 1
# echo "Rebooting in 1 seconds!"
# sleep 1
# echo "Rebooting now!  Your Pi wake up with a freshly updated Raspberry Pi!"
# sleep 1
# sudo reboot
