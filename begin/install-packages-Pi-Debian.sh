#!/bin/bash

PACKAGES=
PACKAGES="$PACKAGES git vim ctags cscope dos2unix wget curl rsync samba"
PACKAGES="$PACKAGES python python-pip fail2ban supervisor htop tree tmux"

# Install all packages on Raspberry Pi Debian system
for package in $PACKAGES; do
	echo "Install package \`$package'..."
	sudo apt-get -y install $package >> install.log
done

