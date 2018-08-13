#!/bin/bash

printf "Breakout Garden: Auto Installer\n\n"

if [ $(id -u) -ne 0 ]; then
	printf "Script must be run as root. Try 'sudo ./install.sh'\n"
	exit 1
fi

printf "Please plug the breakouts you would like to install into your Breakout Garden\n"
read -p "Press any key to continue..."
printf "\n"

WORKING_DIR=`pwd`

python autodetect.py --install | while read line; do
	printf "Found $line\n"
	cd /tmp
	git clone https://github.com/pimoroni/$line
	cd $line
	./install.sh
	cd $WORKING_DIR
done

printf "\nBreakout Garden setup complete! Enjoy your breakouts.\n"
