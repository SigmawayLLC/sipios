import wx
import os
import sys
import pickle
from datetime import datetime
import subprocess
from collections import Counter
import threading
import psutil
import signal
try:
	import auto_detect_robot
except:
	pass

robots = {}


#	This program runs various update programs for Sipi for Robots, from Sigmaway.
#	See more about Sigmaway at http://www.sigmaway.us
'''
	This program is started from the script /home/pi/si_update/sipios/update_master.sh
	From this program you will be able to:
		1.  Update the OS.  This should update the Raspbian operating system.
		2.  Update SGMW Software.   This will update the Raspbian for Robots software, including the source and example files.
		

	Initially Authored:		10/4/2017
	Last Update:			5/6/2017
'''

# Developer Notes and References:
# http://www.blog.pythonlibrary.org/2010/03/18/wxpython-putting-a-background-image-on-a-panel/
# ComboBoxes!  		http://wiki.wxpython.org/AnotherTutorial#wx.ComboBox

image_xpos = 200
image_ypos = 20

# Writes debug to file "error_log"
def write_debug(in_string):
	# In in time logging.
	#print in_string
	write_string = str(datetime.now()) + " - " + in_string + "\n"
	error_file = open('error_log', 'a')		# File: Error logging
	error_file.write(write_string)
	error_file.close()

def detect():
	try:
		detected_robots=auto_detect_robot.autodetect()
		print (detected_robots)
		# handling it this way to cover the cases of 
		# multiple robot detection
		if detected_robots.find("GoPiGo")==0:
			write_state("GoPiGo")
		elif detected_robots.find("BrickPi3")==0:
			write_state("BrickPi3")
		elif detected_robots.find("GrovePi")==0:
			write_state("GrovePi")
		else:
			write_state('sig')
	except:
			write_state("sig")

def write_state(in_string):
	try:
		error_file = open('/home/pi/si_update/sipios/update_gui_elements/selected_state', 'w')		# File: selected state
		if(' ' in in_string): 
			in_string = "sig"
		error_file.write(in_string)
		error_file.close()
	except:
		pass

def read_state():
	error_file = open('/home/pi/si_update/sipios/update_gui_elements/selected_state', 'r')		# File: selected state
	in_string = ""
	in_string = error_file.read()
	error_file.close()
	return in_string


	
def send_bash_command(bashCommand):
	# print bashCommand
	write_debug(bashCommand)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE) #, stderr=subprocess.PIPE)
	# print process
	output = process.communicate()[0]
	# print output
	return output

def send_bash_command_in_background(bashCommand):
	# Fire off a bash command and forget about it.
	write_debug(bashCommand)
	process = subprocess.Popen(bashCommand.split())

########################################################################
class MainPanel(wx.Panel):
	""""""
	#----------------------------------------------------------------------
	def __init__(self, parent):
		global robots
		global update_firmware_static
		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.frame = parent
 
		sizer = wx.BoxSizer(wx.VERTICAL)
		hSizer = wx.BoxSizer(wx.HORIZONTAL)
 
		#wx.StaticText(self, -1, "Raspbian For Robots Update", (25, 5))					# (Minus 50, minus 0)
 
		#-------------------------------------------------------------------
		# Standard Buttons

# removing option to do a Raspbian Update------------------------------------------------
		# Update Raspbian
		#update_raspbian = wx.Button(self, label="Update Raspbian", pos=(20,40))
		#update_raspbian.Bind(wx.EVT_BUTTON, self.update_raspbian)
# ---------------------------------------------------------------------------------------
		
		yoffset = -80
		
		# remove checkboxes
		# wx.StaticBox(self,-1,"Update Sigmaway Software for:",(20,78+yoffset),size=(190,110))
		# for i in range(len(robots_names)):
		# 	posx=35+(110-35)*(i/2)   # result is either 25 or 110
		# 	posy=100+yoffset+(120-100)*(i%2) # result is either 90 or 115
		# 	robots[robots_names[i]]=wx.CheckBox(self,label=robots_names[i], pos=(posx,posy))
		# 	robots[robots_names[i]].SetValue(True)
		# 	robots[robots_names[i]].Bind(wx.EVT_CHECKBOX,self.which_robot)

		# Update DI Software
		update_software = wx.Button(self, label="Update Sigmaway Software", pos=(35,142+yoffset),size=(165,30))
		update_software.Bind(wx.EVT_BUTTON, self.update_software)	
		button_size=update_software.GetSize()
		print button_size


		# Exit
		exit_button = wx.Button(self, label="Exit", pos=(275,250))
		exit_button.Bind(wx.EVT_BUTTON, self.onClose)

	

		#-------------------------------------------------------------------
		# Update Firmware

		yoffset = -70
		#firmware_box = wx.StaticBox(self,-1,"Update Robot:",(20,186+yoffset),size=(190,100))
		#firmware_box.Hide()
		#firmware_box.Bind(wx.EVT_ENTER_WINDOW, self.hovertxt_on)
		#firmware_box.Bind(wx.EVT_LEAVE_WINDOW, self.hovertxt_off)
		# Drop Boxes
		controls = ['Choose your robot', 'coming soon']	# Options for drop down.

		# Select Platform.
		folder = read_state()
		if folder in controls[1:]: # skip 'Choose your robot'
			print("setting drop down to {}".format(folder))
			robotDrop = wx.ComboBox(self, -1, str(folder), pos=(35, 207+yoffset), size=(button_size.GetWidth(), -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		else:
			print ('default drop down')
			robotDrop = wx.ComboBox(self, -1, "Choose your Robot", pos=(35, 207+yoffset), size=(button_size.GetWidth(), -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		robotDrop.Bind(wx.EVT_COMBOBOX, self.robotDrop)					# Binds drop down.		
		#robotDrop.Bind(wx.EVT_ENTER_WINDOW, self.hovertxt_on)
		#robotDrop.Bind(wx.EVT_LEAVE_WINDOW, self.hovertxt_off)

		update_firmware = wx.Button(self, label="Update Robot", pos=(35,242+yoffset),size=(button_size.GetWidth(),-1))
		#print(update_firmware.GetSize())
		update_firmware.Bind(wx.EVT_BUTTON, self.update_firmware)
		update_firmware.Bind(wx.EVT_ENTER_WINDOW, self.hovertxt_on)
		update_firmware.Bind(wx.EVT_LEAVE_WINDOW, self.hovertxt_off)

		update_firmware_static = wx.StaticText(self,-1,"Use this to update the robot firmware.\nThis only needs to be done occasionally! \nIf you have questions, \nplease ask on our forums!",(35,282+yoffset))
		update_firmware_static.Hide()


		
		# Drop Boxes
		#-------------------------------------------------------------------
		
		hSizer.Add((1,1), 1, wx.EXPAND)
		hSizer.Add(sizer, 0, wx.TOP, 100)
		hSizer.Add((1,1), 0, wx.ALL, 75)
		self.SetSizer(hSizer)
	
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)		# Sets background picture
 
		#send_bash_command_in_background("clear")

	#----------------------------------------------------------------------
	def OnEraseBackground(self, evt):
		"""
		Add a picture to the background
		"""
		# yanked from ColourDB.py
		dc = evt.GetDC()
 
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		dc.Clear()	
		# bmp = wx.Bitmap("/home/pi/Desktop/DexterEd/Scratch_GUI/dex.png")	# Draw the photograph.
		# dc.DrawBitmap(bmp, 0, 400)						# Absolute position of where to put the picture
		
		# Add a second picture.
		robot = "/home/pi/si_update/Sipi_For_Robots/update_gui_elements/"+read_state()+".png"
		bmp = wx.Bitmap(robot)	# Draw the photograph.
		dc.DrawBitmap(bmp, image_xpos, image_ypos)	
		
	# RobotDrop
	# This is the function called whenever the drop down box is called.
	def robotDrop(self, event):
		write_debug("robotDrop Selected.")
		controls = ['sig']	# Options for drop down.
		value = event.GetSelection()
		print controls[value]
		# position = 0					# Position in the key list on file
		write_state(controls[value]) 	# print value to file.  
		
		# Update Picture
		robot = "/home/pi/si_update/sipios/update_gui_elements/"+read_state()+".png"
		png = wx.Image(robot, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		wx.StaticBitmap(self, -1, png, (image_xpos, image_ypos), (png.GetWidth(), png.GetHeight()))

	# keep track of which robots to update
	# def which_robot(self,event):
		#print("which_robot called")
		#for i in range(len(robots)):
		#	print robots_names[i], robots[robots_names[i]].GetValue()
		# write_robots_to_update()  # Taking out for now.  This would update the robots to update file.


	# Update the Operating System.
	def update_raspbian(self, event):
		write_debug("update_raspbian")
		dlg = wx.MessageDialog(self, 'Operating System Update will start!  Depending on your internet speed this could take a few hours.  Please do not close the terminal window or restart the update.', 'Alert!', wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
		ran_dialog = False
		if dlg.ShowModal() == wx.ID_OK:
			start_command = "sudo sh /home/pi/si_update/sipios/update_os.sh"
			send_bash_command_in_background(start_command)
			print "Start Operating System update!"
			ran_dialog = True
		else:
			print "Cancel Operating System Update!"
		dlg.Destroy()
		
		write_debug("Cancel Operating System Update.")

	# Update the Software.
	def update_software(self, event):
		write_debug("Update Sigmaway Software")	
		# write_robots_to_update() # Taking out for now.  This would update the write_robots_to_update file.
		dlg = wx.MessageDialog(self, 'Software update will start.  Please do not close the terminal window or restart the update.', 'Alert!', wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
		
		ran_dialog = False
		if dlg.ShowModal() == wx.ID_OK:
			start_command = "sudo bash /home/pi/si_update/sipios/script/update_all.sh"
			send_bash_command_in_background(start_command)
			print "Start software update!"
			ran_dialog = True
		else:
			print "Cancel Software Update!"
		dlg.Destroy()
		
		write_debug("Update Sigmaway Software Finished.")
		
	

	def hovertxt_on(self,event):
		#print("HOVERING")
		update_firmware_static.Show()
		event.Skip()

	def hovertxt_off(self,event):
		#print("HOVERING")
		update_firmware_static.Hide()
		event.Skip()
    
	def onClose(self, event):	# Close the entire program.
		write_debug("Close Pressed.")
		# dlg = wx.MessageDialog(self, 'The Pi will now restart.  Please save all open files before pressing OK.', 'Alert!', wx.OK|wx.ICON_INFORMATION)
		# dlg.ShowModal()
		# dlg.Destroy()
		dlg = wx.MessageDialog(self, 'You must reboot for changes to take effect.  Reboot now?', 'Reboot', wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
		if dlg.ShowModal() == wx.ID_OK:
			# Reboot
			send_bash_command('sudo reboot')
		else: 
			# Do nothing.
			print "No reboot."
		dlg.Destroy()
		"""
		"""
		self.frame.Close()

  
########################################################################
class MainFrame(wx.Frame):
	""""""
	
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		# wx.ComboBox

		wx.Icon('/home/pi/si_update/sipios/update_gui_elements/favicon.ico', wx.BITMAP_TYPE_ICO)
		wx.Log.SetVerbose(False)
		wx.Frame.__init__(self, None, title="Sigmaway Update", size=(400,300))		# Set the frame size

		panel = MainPanel(self)        
		self.Center()
 
########################################################################
class Main(wx.App):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self, redirect=False, filename=None):
		"""Constructor"""
		wx.App.__init__(self, redirect, filename)
		dlg = MainFrame()
		dlg.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
	send_bash_command_in_background("xhost +")
	write_debug(" # Program # started # !")
	detect()
	# reset_file()	#Reset the file every time we turn this program on.
	app = Main()
	app.MainLoop()
