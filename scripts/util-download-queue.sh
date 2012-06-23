#!/bin/bash

##############################################################################
# This routine is used to do download tasks. After all tasks done, it will 
# shutdown the computer.
##############################################################################

HOME=/home/cugfeng
DQ_HOME=$HOME/.dqueue
DQ_TASK=$DQ_HOME/task_list
DQ_DONE=$DQ_HOME/done_list
DQ_STARTED=$DQ_HOME/started

function _is_root()
{
	if [ "`id -u`" = "0" ]; then
		echo true
	else
		echo false
	fi
}

function _dq_init()
{
	if [ ! -d $DQ_TASK ]; then
		mkdir -p $DQ_TASK
	fi
	if [ ! -d $DQ_DONE ]; then
		mkdir -p $DQ_DONE
	fi
}

function _dq_dequeue()
{
	ls $DQ_TASK/*.sh 2>/dev/null | tr '[:space:]' ' ' | awk '{print $1}'
} 

function dq_add()
{
	local _script=`date +%Y%m%d-%H%M%S`.sh
	local _dir=`pwd`
	local _task=$@

	cat >$DQ_TASK/$_script << EOF
pushd $_dir
$_task
popd
EOF
}

function dq_del()
{
	local _task_num=$1
	local _task_name=
	local _task_total=`ls $DQ_TASK/*.sh 2>/dev/null | wc -w`
	local _is_delete=false

	if [ "$_task_total" -eq "0" ]; then
		echo "[Error] Download queue is empty." >&2
	elif [ -f "$DQ_STARTED" ]; then
		echo "[Error] You can not delete when task running." >&2
	else
		if [ "$_task_num" -gt "0" ] && [ "$_task_num" -le "$_task_total" ]; then
			_is_delete=true
		else
			echo "[Error] Index out of range[1, "$_task_total"]." >&2 
		fi
	fi

	if [ "$_is_delete" = "true" ]; then
		_task_name=`ls $DQ_TASK/*.sh | tr '[:space:]' ' ' | cut -d ' ' -f $_task_num`
		rm -f $_task_name
	fi
}

function dq_list()
{
	local _index=1
	local _script=
	local _task=
	
	for _script in `ls $DQ_TASK/*.sh 2>/dev/null`; do
		_task=`head -2 $_script | tail -1`
		
		printf "%d.\t%s\n" "$_index" "$_task"
		_index=`expr $_index + 1`
	done
}

function dq_cleanup()
{
	rm -f $DQ_STARTED
}

function dq_start()
{
	local _cur_task=

	touch $DQ_STARTED
	if [ "`_is_root`" = true ]; then
		while [ 1 ]; do
			_cur_task=`_dq_dequeue`
			if [ -n "$_cur_task" ]; then
				bash $_cur_task
				if [ $? -eq 0 ]; then
					mv $_cur_task $DQ_DONE
				fi
			else
				echo "[Info] All tasks done."
				break
			fi
		done
	else
		echo "[Error] You must be root to run dq_start." >&2
	fi
	dq_cleanup

	shutdown -h 1
}

_dq_init

