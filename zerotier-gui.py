#!/usr/bin/sudo python3
#
#A Linux front-end for ZeroTier
#Copyright (C) 2020  Tomás Ralph
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################

import json, subprocess
import tkinter as tk
from tkinter import messagebox

class MainWindow:

	def __init__(self):

		# create widgets
		# window setup
		self.window = tk.Tk()
		self.window.title("ZeroTier One")
		self.window.resizable(width = False, height = False)

		# layout setup
		self.topFrame = tk.Frame(self.window, padx = 20, pady = 10)
		self.middleFrame = tk.Frame(self.window, padx = 20)
		self.bottomFrame = tk.Frame(self.window, padx = 20, pady = 10)

		# widgets
		self.networkLabel = tk.Label(self.topFrame, text="Joined Networks:", font=40)
		self.refreshButton = tk.Button(self.topFrame, text="Refresh Networks", bg="#ffb253", activebackground="#ffbf71", command=self.refresh_networks)
		self.joinButton = tk.Button(self.topFrame, text="Join Network", bg="#ffb253", activebackground="#ffbf71", command=self.join_network_window)

		self.networkListScrollbar = tk.Scrollbar(self.middleFrame)
		self.networkList = tk.Listbox(self.middleFrame, width="100", height="15", font="Monospace", selectmode="single")
		self.networkList.bind('<Double-Button-1>', self.call_see_network_info)

		self.leaveButton = tk.Button(self.bottomFrame, text="Leave Network", bg="#ffb253", activebackground="#ffbf71", command=self.leave_network)
		self.infoButton = tk.Button(self.bottomFrame, text="Network Info", bg="#ffb253", activebackground="#ffbf71", command=self.see_network_info)

		# pack widgets
		self.networkLabel.pack(side="left", anchor="sw")
		self.refreshButton.pack(side="right", anchor="se")
		self.joinButton.pack(side="right", anchor="se")

		self.networkListScrollbar.pack(side="right", fill="both")
		self.networkList.pack(side="bottom", fill="x")

		self.leaveButton.pack(side="left", fill="x")
		self.infoButton.pack(side="right", fill="x")

		# frames
		self.topFrame.pack(side="top", fill="x")
		self.middleFrame.pack(side = "top", fill = "x")
		self.bottomFrame.pack(side = "top", fill = "x")

		# extra configuration
		self.refresh_networks()

		self.networkList.config(yscrollcommand=self.networkListScrollbar.set)
		self.networkListScrollbar.config(command=self.networkList.yview)

	def call_see_network_info(self, event):
		self.see_network_info()

	def refresh_networks(self):

		self.networkList.delete(0, 'end')
		networks = []
		# outputs info of networks in json format
		networkData = self.get_networks_info()

		# get networks id
		for network in range(len(networkData)):
			networks.append((networkData[network]['nwid'], networkData[network]['name'], networkData[network]['status']))


		# set networks in widget
		for networkId, networkName, networkStatus in networks:
			if not networkName:
				networkName = "No name"
			self.networkList.insert('end', '{} | {:55s} |{}'.format(networkId, networkName, networkStatus))

	def get_networks_info(self):
		return json.loads(subprocess.check_output(['zerotier-cli', '-j', 'listnetworks']))

	def launch_sub_window(self):
		return tk.Toplevel(self.window)

	def join_network_window(self):

		def join_network(network):

			try:
				subprocess.check_output(['zerotier-cli', 'join', network])
				joinResult = "Successfully joined network"
			except:
				joinResult = "Invalid network ID"
			messagebox.showinfo(icon="info", message=joinResult)
			self.refresh_networks()

			joinWindow.destroy()

		joinWindow = self.launch_sub_window()

		# widgets
		mainFrame = tk.Frame(joinWindow, padx = 20, pady = 20)

		joinLabel = tk.Label(mainFrame, text="Network ID:")
		networkIdEntry = tk.Entry(mainFrame, font="Monospace")
		joinButton = tk.Button(mainFrame, text="Join", bg="#ffb253", activebackground="#ffbf71", command=lambda: join_network(networkIdEntry.get()))

		# pack widgets
		joinLabel.pack(side="top", anchor="w")
		networkIdEntry.pack(side="top", fill="x")
		joinButton.pack(side="top", fill="x")

		mainFrame.pack(side="top", fill="x")

	def leave_network(self):

		# get selected network
		network = self.networkList.get('active')
		network = network[:network.find(" ")]

		try:
			subprocess.check_output(['zerotier-cli', 'leave', network])
			leaveResult = "Successfully left network"
		except:
			leaveResult = "Error"
		messagebox.showinfo(icon="info", message=leaveResult)
		self.refresh_networks()

	def see_network_info(self):

		# setting up
		try:
			idInList = self.networkList.curselection()[0]
		except:
			messagebox.showinfo(icon="info", title="Error", message="No network selected")
			return

		infoWindow = self.launch_sub_window()

		# id in list will always be the same as id in json
		currentNetworkInfo = self.get_networks_info()[idInList]

		# frames
		topFrame = tk.Frame(infoWindow, pady=30)
		middleFrame = tk.Frame(infoWindow, padx=20)

		allowDefaultFrame = tk.Frame(infoWindow, padx=20)
		allowGlobalFrame = tk.Frame(infoWindow, padx=20)
		allowManagedFrame = tk.Frame(infoWindow, padx=20)

		bottomFrame = tk.Frame(infoWindow, pady=10)

		# check variables
		allowDefault = tk.BooleanVar()
		allowGlobal = tk.BooleanVar()
		allowManaged = tk.BooleanVar()

		allowDefault.set(currentNetworkInfo['allowDefault'])
		allowGlobal.set(currentNetworkInfo['allowGlobal'])
		allowManaged.set(currentNetworkInfo['allowManaged'])

		# assigned addresses text generation
		assignedAddresses = ""
		for address in currentNetworkInfo['assignedAddresses']:
			assignedAddresses += address + " "

		# widgets
		titleLabel = tk.Label(topFrame, text="Network Info", font=70)

		nameLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Name:", currentNetworkInfo['name']))
		nwIdLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Network ID:", currentNetworkInfo['nwid']))
		assignedAddrLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Assigned Addresses:", assignedAddresses))
		statusLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Status:", currentNetworkInfo['status']))
		typeLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Type:", currentNetworkInfo['type']))
		deviceLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Device:", currentNetworkInfo['portDeviceName']))
		bridgeLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Bridge:", currentNetworkInfo['bridge']))
		macLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("MAC Address:", currentNetworkInfo['mac']))
		mtuLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("MTU:", currentNetworkInfo['mtu']))
		dhcpLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("DHCP:", currentNetworkInfo['dhcp']))

		allowDefaultLabel = tk.Label(allowDefaultFrame, font="Monospace", text="{:24s}".format("Allow Default Route"))
		allowDefaultCheck = tk.Checkbutton(allowDefaultFrame, variable=allowDefault, command=lambda: change_config("allowDefault", allowDefault.get()))

		allowGlobalLabel = tk.Label(allowGlobalFrame, font="Monospace", text="{:24s}".format("Allow Global IP"))
		allowGlobalCheck = tk.Checkbutton(allowGlobalFrame, variable=allowGlobal, command=lambda: change_config("allowGlobal", allowGlobal.get()))

		allowManagedLabel = tk.Label(allowManagedFrame, font="Monospace", text="{:24s}".format("Allow Managed IP"))
		allowManagedCheck = tk.Checkbutton(allowManagedFrame, variable=allowManaged, command=lambda: change_config("allowManaged", allowManaged.get()))

		closeButton = tk.Button(bottomFrame, text="Ok", bg="#ffb253", activebackground="#ffbf71", command=lambda: infoWindow.destroy())

		# pack widgets
		titleLabel.pack(side="top", anchor="n")

		nameLabel.pack(side="top", anchor="w")
		nwIdLabel.pack(side="top", anchor="w")
		assignedAddrLabel.pack(side="top", anchor="w")
		statusLabel.pack(side="top", anchor="w")
		typeLabel.pack(side="top", anchor="w")
		deviceLabel.pack(side="top", anchor="w")
		bridgeLabel.pack(side="top", anchor="w")
		macLabel.pack(side="top", anchor="w")
		mtuLabel.pack(side="top", anchor="w")
		dhcpLabel.pack(side="top", anchor="w")

		allowDefaultLabel.pack(side="left", anchor="w")
		allowDefaultCheck.pack(side="left", anchor="w")

		allowGlobalLabel.pack(side="left", anchor="w")
		allowGlobalCheck.pack(side="left", anchor="w")

		allowManagedLabel.pack(side="left", anchor="w")
		allowManagedCheck.pack(side="left", anchor="w")

		closeButton.pack(side="top")

		topFrame.pack(side="top", fill="both")
		middleFrame.pack(side="top", fill="both")

		allowDefaultFrame.pack(side="top", fill="both")
		allowGlobalFrame.pack(side="top", fill="both")
		allowManagedFrame.pack(side="top", fill="both")

		bottomFrame.pack(side="top", fill="both")

		# checkbutton functions
		def change_config(config, value):

			# zerotier-cli only accepts int values
			if value:
				value = 1
			else:
				value = 0

			subprocess.check_output(['zerotier-cli', 'set', currentNetworkInfo['nwid'], f"{config}={value}"])

		# needed to stop local variables from being destroyed before the window
		infoWindow.mainloop()

if __name__ == "__main__":

	# simple check for zerotier
	try:
		subprocess.check_output(['zerotier-cli', '-j', 'listnetworks'])
	except:
		messagebox.showinfo(title="Error", message="The program hasn't been ran as root, or ZeroTier isn't installed or properly configured! Make sure the service 'zerotier-one' is running.", icon="error")
		exit()

	# create mainwindow class and execute the mainloop
	mainWindow = MainWindow().window
	mainWindow.mainloop()
