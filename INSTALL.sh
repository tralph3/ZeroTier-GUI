#!/bin/sh
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

echo "We need root access to change the owner of the script"

chmod +x zerotier-gui
sudo chown root zerotier-gui
sudo chown root zerotier-gui.png
sudo chown root zerotier-gui.desktop
sudo mv -vf zerotier-gui /usr/bin/
sudo mv -vf zerotier-gui.png /usr/share/pixmaps/
sudo mv -vf zerotier-gui.desktop /usr/share/applications/
