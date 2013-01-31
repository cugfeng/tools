#!/bin/bash

PACKAGE_LIST="build-essential git vim ctags cscope tree htop samba curl"

for package in $PACKAGE_LIST; do
	echo "Install package \`$package'..."
	sudo apt-get -y install $package >> install.log
done

