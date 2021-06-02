# ZeroTier-GUI <img src="img/zerotier-gui.png" align="bottom">

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/tralph3/ZeroTier-GUI?style=flat-square)](https://github.com/tralph3/ZeroTier-GUI/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=flat-square)](https://github.com/tralph3/ZeroTier-GUI/blob/master/LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg?style=flat-square)](https://paypal.me/tralph3)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-☕-yellow.svg?style=flat-square)](https://www.buymeacoffee.com/tralph3)

**A Linux front-end for ZeroTier**

### Manage Networks
<img src="img/managenetworks1.png " width="1000">
<img src="img/managenetworks2.png " width="1000">

### Manage Peers
<img src="img/managepeers.png " width="500">

# Installation

You can download the software from the [AUR](https://aur.archlinux.org/packages/zerotier-gui-git/).

    paru -Syu zerotier-gui-git

If you are in an Ubuntu/Debian based distribution, you can download the source code and run the `make_deb.sh` script.

    ZeroTier-GUI$ cd packaging
    ZeroTier-GUI$ ./make_deb.sh

You may need to mark it as executable first:

    chmod +x make_deb.sh

**The script must be ran on the `packaging` folder, make sure to `cd` into it.**

The script will generate a `ZeroTier-GUI.deb` package in the root directory. Simply install it with `dpkg -i Zerotier-GUI.deb`. You may need to run `apt -f install` afterwards to install dependencies if unmet.

# Dependencies

None of the packages contains the back-end, zerotier-one. Arch has it in the `community` repo. For Ubuntu based distributions, you'll need to install it manually [from their website](https://www.zerotier.com/download/). On top of that, you'll need python3.6 or greater, and the tkinter module. This however should be handled by the packaging software.
