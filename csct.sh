#!/bin/bash

version=1.0.2
date=2011-12-01

cs_file=cscope.files
lookup_file=filenametags
clean_file_list="$cs_file cscope.in.out cscope.po.out cscope.out tags $lookup_file"

function gen_file_list()
{
	local _file_list=$@
	
	rm -f $cs_file
	for _file in $_file_list; do
		if [ -f $_file ]; then
			echo `pwd`/$_file >> $cs_file
		elif [ -d $_file ]; then
			find `pwd`/$_file -regex ".*\.\(h\|c\|cpp\|java\)" -type f >> $cs_file 2>/dev/null
		else
			echo "Warning: ignore \`$_file'" >&2
		fi
	done
}

function gen_symbol_list()
{
	if [ -f $cs_file ]; then
		cscope -bkq -i $cs_file
		ctags -L $cs_file
	fi
}

function gen_lookup_file_list()
{
	local _tmp_file=$cs_file.sorted
	
	rm -f $_tmp_file
	if [ -f $cs_file ]; then
		for file in `cat $cs_file`; do
			printf "%s\t%s\t1\n" `basename $file` $file >> $_tmp_file
		done
		echo -e "!_TAG_FILE_SORTED\t2\t/2=foldcase/" > $lookup_file
		cat $_tmp_file | sort -f >> $lookup_file
	fi
}

function clean()
{
	rm -f $clean_file_list
}

function show_usage()
{
	echo "Usage:"
	echo "    $(basename $0) [-f | -s | -c | -l | -h | -v]"
	echo "    Generate symbol list use cscope and ctags"
	echo "Options:"
	echo "    -f | --filelist  : generate file list"
	echo "    -s | --symbollist: generate symbol list"
	echo "    -c | --clean     : clean cscope and ctags file"
	echo "    -l | --lookupfile: generate lookup file list"
	echo "    -h | --help      : show help"
	echo "    -v | --version   : show version"
	echo ""

	exit 0
}

function show_version()
{
	echo "Version: $version"
	echo "Date   : $date"

	exit 0
}

b_gen_file_list=false
b_gen_symbol_list=false
b_clean=false
b_gen_lookup_file_list=false
file_list=

while [ -n "$1" ]; do
	case "$1" in
		-f|--filelist)
			b_gen_file_list=true
			shift
			;;

		-s|--symbollist)
			b_gen_symbol_list=true
			shift
			;;

		-c|--clean)
			b_clean=true
			shift
			;;

		-l|--lookupfile)
			b_gen_lookup_file_list=true
			shift
			;;

		-h|--help)
			show_usage
			;;

		-v|--version)
			show_version
			;;

		*)
			file_list="$file_list $(pwd)/$1"
			shift
			;;
	esac
done

if [ $b_clean = "true" ]; then
	clean
	exit 0
fi

if [ "$b_gen_file_list" = "false" ] && [ "$b_gen_symbol_list" = "false" ] \
	   && [ "$b_gen_lookup_file_list" = "false" ]; then
	b_gen_file_list=true
	b_gen_symbol_list=true
	b_gen_lookup_file_list=true
fi

if [ $b_gen_file_list = "true" ]; then
	if [ -z "$file_list" ]; then
		file_list=.
	fi
	gen_file_list $file_list
fi

if [ $b_gen_symbol_list = "true" ]; then
	gen_symbol_list
fi

if [ $b_gen_lookup_file_list = "true" ]; then
	gen_lookup_file_list
fi

