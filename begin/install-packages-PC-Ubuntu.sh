#!/bin/bash

PACKAGES="build-essential git vim ctags cscope tree htop samba curl gparted vlc"

for package in $PACKAGES; do
	echo "Install package \`$package'..."
	sudo apt-get -y install $package >> install.log
done

