#!/bin/bash

######################################################################
#                        Test Path Utiliti
#
# When meet a complie error, it says /a/b/c/d.c was not found, but 
# we don't know whether the directory or the file not exist. This 
# utiliti will locate the directory/file does not exitst immediately.
#
######################################################################

function tp()
{
	local _path=$1

	local _prefix=${_path:0:1}
	if [ "$_prefix" != "/" ]; then
		_prefix=
	fi

	local _nodes=$(echo $_path | tr -s "/" " ")
	local _num=$(echo $_nodes | wc -w)
	for ((i=0; i<$_num; i++)); do
		local _curr="$_prefix"
		local _j=0
		for _node in $_nodes; do
			if [ $_j -eq 0 ]; then
				_curr="$_curr$_node"
			else 
				_curr="$_curr/$_node"
			fi
			_j=$(expr $_j + 1)
			if [ $_j -gt $i ]; then
				break
			fi
		done

		if [ $i -lt $(expr $_num - 1) ]; then
			if [ ! -d "$_curr" ]; then
				echo "[Error] Directory '$_curr' dose not exist!"
				return
			fi
		else
			if [ ! -d "$_curr" -a ! -f "$_curr" ]; then
				echo "[Error] '$_curr' does not exist!"
				return
			fi
		fi
	done				
}

