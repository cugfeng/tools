#!/bin/bash

GITHUB=$HOME/github
TOOLS=$HOME/tools

[ -d $GITHUB ] || mkdir -p $GITHUB
cd $GITHUB && git clone https://github.com/cugfeng/tools.git

BASH_FILES=".bash_aliases .bash_user .tmux.conf .gitconfig"
VIM_FILES=".vim .vimrc"

[ -d $TOOLS ] || mkdir -p $TOOLS
for file in $BASH_FILES; do
	cp -rf $GITHUB/tools/bash/$file $HOME
done
for file in $VIM_FILES; do
	cp -rf $GITHUB/tools/vim/$file $HOME
done
cp -rf $GITHUB/tools/bin $TOOLS
chmod u+x $TOOLS/bin/*
cp -rf $GITHUB/tools/scripts $TOOLS

