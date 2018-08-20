#!/bin/bash

printf "Breakout Garden: Auto Installer\n\n"

if [ $(id -u) -ne 0 ]; then
	printf "Script must be run as root. Try 'sudo ./install.sh'\n"
	exit 1
fi

printf "Please plug the breakouts you would like to install into your Breakout Garden\n\n"
read -p "Press enter to continue..."
printf "\n"

WORKING_DIR=`pwd`
TMP_DIR="/tmp/breakout-garden"

results=`python autodetect.py`
found=`echo "$results" | wc -l`

if [[ "$found" -eq "0" ]] || [[ "$results" == "" ]]; then
	printf "Sorry, I couldn't find any breakouts!\n"
	exit 1
fi

printf "Found $found breadkout(s):\n"

echo "$results" | while read line; do
	printf "$line\n"
done

printf "\n"

read -p "Press enter to continue..."

if [[ ! -d "$TMP_DIR" ]]; then
	mkdir "$TMP_DIR"
fi

python autodetect.py --install | while read line; do
	printf "Installing $line\n"
	git_dir="$line"
	cd $TMP_DIR
	if [[ ! -d "$git_dir/.git" ]]; then
		rm -f $git_dir
		git clone https://github.com/pimoroni/$line $git_dir
	fi
	cd $git_dir
	git pull origin master
	if [[ -f "install.sh" ]]; then
		./install.sh
	else
		printf "Warning: No install.sh found for $line. Skipping!";
	fi
	cd $WORKING_DIR
done

printf "\nBreakout Garden setup complete! Enjoy your breakouts.\n"
