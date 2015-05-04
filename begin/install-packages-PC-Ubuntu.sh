#!/bin/bash

ADMIN="openssh-server tree htop samba curl zsh tmux autojump"
DEV="git vim ctags cscope dos2unix"
BUILD="ccache build-essential zlib1g-dev libssl-dev libbz2-dev"

PACKAGES="$ADMIN $DEV $BUILD"
for package in $PACKAGES; do
	echo "Install package \`$package'..."
	sudo apt-get -y install $package >> install.log
done

