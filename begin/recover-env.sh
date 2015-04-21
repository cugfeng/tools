#!/bin/bash

G_TOOLS=$HOME/github/tools
H_TOOLS=$HOME/tools

CFG_FILES=".sh_aliases .sh_user .tmux.conf .gitconfig"
VIM_FILES=".vim .vimrc"
BIN_FILES="bin python shell"

if [ ! -d $G_TOOLS ]; then
	echo "Please run command below to clone from github:"
	echo "    mkdir -p $HOME/github && cd $HOME/github"
	echo "    git clone https://github.com/cugfeng/tools.git"
	echo

	exit 0
fi

for file in $CFG_FILES; do
	cp -rf $G_TOOLS/config/$file $HOME
done
for file in $VIM_FILES; do
	cp -rf $G_TOOLS/vim/$file $HOME
done

[ -d $H_TOOLS ] || mkdir -p $H_TOOLS
for file in $BIN_FILES; do
	cp -rf $G_TOOLS/$file $H_TOOLS
done

# Install oh my zsh and configure it
wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | sh
cd $HOME && patch -p0 < $G_TOOLS/config/zshrc.patch

