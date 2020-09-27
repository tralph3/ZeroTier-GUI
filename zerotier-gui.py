#!/usr/bin/env python3
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

import tkinter as tk
from tkinter import messagebox
from subprocess import check_output, STDOUT, CalledProcessError
from json import loads
from os import getuid, system
from webbrowser import open_new_tab

class MainWindow:

	def __init__(self):

		# create widgets
		# window setup
		self.window = tk.Tk()
		self.window.title("ZeroTier")
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
		self.ztCentralButton = tk.Button(self.bottomFrame, text="ZeroTier Central", bg="#ffb253", activebackground="#ffbf71", command=self.zt_central)
		self.toggleConnectionButton = tk.Button(self.bottomFrame, text="Disconnect/Connect Interface", bg="#ffb253", activebackground="#ffbf71", command=self.toggle_interface_connection)
		self.infoButton = tk.Button(self.bottomFrame, text="Network Info", bg="#ffb253", activebackground="#ffbf71", command=self.see_network_info)

		# pack widgets
		self.networkLabel.pack(side="left", anchor="sw")
		self.refreshButton.pack(side="right", anchor="se")
		self.joinButton.pack(side="right", anchor="se")

		self.networkListScrollbar.pack(side="right", fill="both")
		self.networkList.pack(side="bottom", fill="x")

		self.leaveButton.pack(side="left", fill="x")
		self.toggleConnectionButton.pack(side="left", fill="x")
		self.infoButton.pack(side="right", fill="x")
		self.ztCentralButton.pack(side="right", fill="x")

		# frames
		self.topFrame.pack(side="top", fill="x")
		self.middleFrame.pack(side = "top", fill = "x")
		self.bottomFrame.pack(side = "top", fill = "x")

		# extra configuration
		self.refresh_networks()

		self.networkList.config(yscrollcommand=self.networkListScrollbar.set)
		self.networkListScrollbar.config(command=self.networkList.yview)

	def zt_central(self):
		open_new_tab("https://my.zerotier.com")

	def call_see_network_info(self, event):
		self.see_network_info()

	def refresh_networks(self):

		self.networkList.delete(0, 'end')
		networks = []
		# outputs info of networks in json format
		networkData = self.get_networks_info()

		# get networks id
		for networkPosition in range(len(networkData)):

			if self.get_interface_state(networkData[networkPosition]['portDeviceName']).lower() == "down":
				isDown = True
			else:
				isDown = False

			networks.append((networkData[networkPosition]['nwid'], networkData[networkPosition]['name'], networkData[networkPosition]['status'], isDown, networkPosition))

		# set networks in widget
		for networkId, networkName, networkStatus, isDown, networkPosition in networks:

			if not networkName:
				networkName = "No name"
			self.networkList.insert('end', '{} | {:55s} |{}'.format(networkId, networkName, networkStatus))

			if isDown:
				self.networkList.itemconfig(networkPosition, bg='red')

	def get_networks_info(self):
		# json.loads
		return loads(check_output(['zerotier-cli', '-j', 'listnetworks']))

	def launch_sub_window(self):
		return tk.Toplevel(self.window)

	def join_network_window(self):

		def join_network(network):

			try:
				check_output(['zerotier-cli', 'join', network])
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
			check_output(['zerotier-cli', 'leave', network])
			leaveResult = "Successfully left network"
		except:
			leaveResult = "Error"
		messagebox.showinfo(icon="info", message=leaveResult)
		self.refresh_networks()

	def get_interface_state(self, interface):

		addressesInfo = check_output(['ip', 'address']).decode()

		stateLine = addressesInfo.find(interface)
		stateStart = addressesInfo.find("state ", stateLine)
		stateEnd = addressesInfo.find(" ", stateStart + 6)
		state = addressesInfo[stateStart + 6:stateEnd]

		return state

	def toggle_interface_connection(self):

		# setting up
		try:
			idInList = self.networkList.curselection()[0]
		except:
			messagebox.showinfo(icon="info", title="Error", message="No network selected")
			return

		# id in list will always be the same as id in json
		# because the list is generated in the same order
		currentNetworkInfo = self.get_networks_info()[idInList]
		currentNetworkInterface = currentNetworkInfo['portDeviceName']

		state = self.get_interface_state(currentNetworkInterface)

		if state.lower() == "down":
			check_output(['pkexec', 'ip', 'link', 'set', currentNetworkInterface, 'up'])
		else:
			check_output(['pkexec', 'ip', 'link', 'set', currentNetworkInterface, 'down'])

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
		# because the list is generated in the same order
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
		assignedAddresses = currentNetworkInfo['assignedAddresses'][0]
		for address in currentNetworkInfo['assignedAddresses'][1:]:
			assignedAddresses += "\n{:>42s}".format(address)

		# widgets
		titleLabel = tk.Label(topFrame, text="Network Info", font=70)

		nameLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Name:", currentNetworkInfo['name']))
		nwIdLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Network ID:", currentNetworkInfo['nwid']))
		assignedAddrLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Assigned Addresses:", assignedAddresses))
		statusLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("Status:", currentNetworkInfo['status']))
		stateLabel = tk.Label(middleFrame, font="Monospace", text="{:25s}{}".format("State:", self.get_interface_state(currentNetworkInfo['portDeviceName'])))
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

		closeButton = tk.Button(bottomFrame, text="Close", bg="#ffb253", activebackground="#ffbf71", command=lambda: infoWindow.destroy())

		# pack widgets
		titleLabel.pack(side="top", anchor="n")

		nameLabel.pack(side="top", anchor="w")
		nwIdLabel.pack(side="top", anchor="w")
		assignedAddrLabel.pack(side="top", anchor="w")
		statusLabel.pack(side="top", anchor="w")
		stateLabel.pack(side="top", anchor="w")
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

			check_output(['zerotier-cli', 'set', currentNetworkInfo['nwid'], f"{config}={value}"])

		# needed to stop local variables from being destroyed before the window
		infoWindow.mainloop()

if __name__ == "__main__":

	def warning_window():
		if getuid() != 0:

			# get username
			username = check_output(['whoami']).decode()
			username = username.replace("\n", "")

			if messagebox.askyesno(icon="info", title="Root access needed", message=f"In order to grant {username} access to ZeroTier we need temporary root access to store the Auth Token in your home folder. Otherwise, you would need to run this program as root. Grant access?"):

				# copy auth token to home directory and make the user own it
				system(f'pkexec bash -c "cp /var/lib/zerotier-one/authtoken.secret /home/{username}/.zeroTierOneAuthToken && chown {username} /home/{username}/.zeroTierOneAuthToken && chmod 0600 /home/{username}/.zeroTierOneAuthToken"')

			else:
				exit()

	# temporary window for popups
	tmp = tk.Tk()
	tmp.withdraw()

	# simple check for zerotier
	try:
		check_output(['zerotier-cli', 'listnetworks'], stderr=STDOUT)

	except CalledProcessError as error:
		output = error.output.decode()

		if "missing authentication token" in output:
			messagebox.showinfo(title="Error", message="This user doesn't have access to ZeroTier!", icon="error")
			warning_window()
		elif "Error connecting" in output:
			messagebox.showinfo(title="Error", message='"zerotier-one" service isn\'t running!', icon="error")
			exit()

	except FileNotFoundError:
		messagebox.showinfo(title="Error", message="ZeroTier isn't installed!", icon="error")
		exit()

	# destroy temporary window
	tmp.destroy()

	# create mainwindow class and execute the mainloop
	mainWindow = MainWindow().window
	mainWindow.mainloop()
