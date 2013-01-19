#!/bin/bash

src_file=".bash_aliases .bash_profile .bashrc .vimrc .sdirs"
src_dir=".vim"

time=`date +%Y%m%d-%H%M%S`
target_dir=$HOME/backup/config/$time

mkdir -p $target_dir
for file in $src_file; do
	cp -f $HOME/$file $target_dir
done
for dir in $src_dir; do
	cp -rf $HOME/$dir $target_dir
done

