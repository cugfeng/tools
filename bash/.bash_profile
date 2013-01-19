if [ -f $HOME/.bashrc ]; then
	source $HOME/.bashrc
fi

# cugfeng bash definitions
SCRIPT_PATH=$HOME/tools/scripts
BIN_PATH=$HOME/tools/bin

for script in $SCRIPT_PATH/util-*.sh; do
	source "$script"
done

PATH=$PATH:$BIN_PATH

