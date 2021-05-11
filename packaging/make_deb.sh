#!/bin/sh

# This script will create a deb package for ZeroTier-GUI

cd ..
packageVersion=$(printf "1.2.1.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)")
cd -

# Create file structure

mkdir -v DEBIAN
mkdir -pv usr/share/{licenses/ZeroTier-GUI,pixmaps,applications,doc/ZeroTier-GUI}
mkdir -pv usr/bin


# Copy files to corresponding directories

cp -vf ../LICENSE usr/share/licenses/ZeroTier-GUI
cp -vf ../img/zerotier-gui.png usr/share/pixmaps
cp -vf ../zerotier-gui.desktop usr/share/applications
cp -vf ../README.md usr/share/doc/ZeroTier-GUI
cp -vf ../src/zerotier-gui usr/bin


# Create control file

echo "Package: zerotier-gui
Version: ${packageVersion}
Architecture: all
Maintainer: tralph3
Depends: python3-tk,policykit-1,python3 (>=3.6)
Priority: optional
Homepage: https://github.com/tralph3/ZeroTier-GUI
Description: A Linux front-end for ZeroTier" > DEBIAN/control

# Build the package

dpkg-deb --build ../packaging

# Rename the package

mv ../packaging.deb ../ZeroTier-GUI.deb
