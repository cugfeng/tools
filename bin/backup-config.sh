#!/bin/bash

src_file=".bash_aliases .bash_user .vimrc .tmux.conf .gitconfig"
src_dir=".vim"

time=`date +%Y%m%d-%H%M%S`
target_dir=$HOME/backup/config/$time

printf "Backup to directory \`%s'..." $target_dir
mkdir -p $target_dir
for file in $src_file; do
	cp -f $HOME/$file $target_dir
done
for dir in $src_dir; do
	cp -rf $HOME/$dir $target_dir
done
printf "Done!\n"

