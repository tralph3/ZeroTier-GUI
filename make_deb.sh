#!/bin/sh

# This script will create a deb package for ZeroTier-GUI

packageVersion=$(printf "1.4.0.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)")

# Create file structure

mkdir -pv packaging/DEBIAN
mkdir -pv packaging/usr/share/licenses/ZeroTier-GUI
mkdir -pv packaging/usr/share/pixmaps
mkdir -pv packaging/usr/share/applications
mkdir -pv packaging/usr/share/doc/ZeroTier-GUI
mkdir -pv packaging/usr/bin


# Copy files to corresponding directories

cp -vf LICENSE packaging/usr/share/licenses/ZeroTier-GUI
cp -vf img/zerotier-gui.png packaging/usr/share/pixmaps
cp -vf zerotier-gui.desktop packaging/usr/share/applications
cp -vf README.md packaging/usr/share/doc/ZeroTier-GUI
cp -vf src/zerotier-gui packaging/usr/bin


# Create control file

echo "Package: zerotier-gui
Version: ${packageVersion}
Architecture: all
Maintainer: tralph3
Depends: python3-tk,policykit-1,python3 (>=3.6)
Priority: optional
Homepage: https://github.com/tralph3/ZeroTier-GUI
Description: A Linux front-end for ZeroTier" > packaging/DEBIAN/control

# Build the package

dpkg-deb --build packaging

# Rename the package

mv packaging.deb ZeroTier-GUI.deb
