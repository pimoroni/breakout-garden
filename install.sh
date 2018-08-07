#!/bin/bash

WORKING_DIR=`pwd`

python autodetect.py --install | while read line; do
	cd /tmp
	git clone https://github.com/pimoroni/$line
	./install.sh
	cd $WORKING_DIR
done
