#! /bin/sh

PACKAGES=
PACKAGES="$PACKAGES smbd samba smbpasswd ftp vim git ctags cscope"
PACKAGES="$PACKAGES omxplayer fbi parted tree screen autossh privoxy"
### For Bit torrent download and web interface ###
PACKAGES="$PACKAGES deluged deluge-console python-mako deluge-web" 

# Install all packages on Raspberry Pi Debian system
for package in $PACKAGES; do
	echo "Install package \`$package'..."
	sudo apt-get -y install $package >> install.log
done

