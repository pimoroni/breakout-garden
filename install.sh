#!/bin/bash

WORKING_DIR=`pwd`
TMP_DIR="/tmp/breakout-garden"
LOG_FILE="$TMP_DIR/install.log"
ACTION="install"
VERBOSE=""
FORCE=""
EVERYTHING=""
PYTHON="/usr/bin/python3"

DEVICES=()
STATUSES=()
REPOS=()

PADDING=5

read -r -d '' USAGE << EOF
Usage:

sudo ./install.sh:
    -h/--help    - print this message.
    -v/--verbose - extra spicy debug output.
    -f/--force   - force install.
    -a/--all     - install *everything* (that breakouts.config knows about)

    
EOF

success() {
	printf "$(tput setaf 2)$1$(tput setaf 7)"
}

inform() {
	printf "$(tput setaf 6)$1$(tput setaf 7)"
}

warning() {
	printf "$(tput setaf 1)$1$(tput setaf 7)"
}

if [ $(id -u) -ne 0 ]; then
	printf "Breakout Garden: Installer\n\n"
	inform "Script must be run as root. Try 'sudo ./install.sh'\n"
	exit 1
fi

if [ ! -c "/dev/i2c-1" ]; then	
	raspi-config nonint do_i2c 0
	STATUS=$?
	if [ $STATUS -eq 0 ]; then
		inform "\nBreakout Garden requires I2C. We've enabled it for you.\n"
	else
		warning "\nWarning, Breakout Garden requires I2C but we couldn't enable it.\n"
		printf "\nPlease try 'curl https://get.pimoroni.com/i2c | bash' to enable I2C first.\n"
		exit 1
	fi
	sleep 0.1
fi

if [ ! -d "$TMP_DIR" ]; then
	mkdir $TMP_DIR
fi


while [[ $# -gt 0 ]]; do
	K="$1"
	case $K in
	-h|--help)
		echo "$USAGE";
		exit 0
		;;
	-a|--all)
		EVERYTHING="true";
		shift
		;;
	-u|--uninstall)
		ACTION="uninstall";VERBOSE="true";
		shift
		;;
	-v|--verbose)
		VERBOSE="true";
		shift
		;;
	-f|--force)
		FORCE="true";
		shift
		;;
	*)
		if [[ $1 == -* ]]; then
			printf "Unrecognised option: $1\n\n";
			echo "$USAGE";
			exit 1
		fi
		POSITION_ARGS+=$("$1")
		shift
	esac
done

# Set the script args to the remaining positional args, so $1 etc work as expected
set -- "${POSITIONAL_ARGS[@]}"

if [[ ! "$EVERYTHING" == "" ]]; then
	DETECTED=`$PYTHON autodetect.py --install --force-all`
else
	DETECTED=`$PYTHON autodetect.py --install`
fi

COUNT=`echo -e "$DETECTED" | wc -l`

if [[ "$COUNT" -eq "0" ]] || [[ "$DETECTED" == "" ]]; then
	printf "Sorry, I couldn't find any breakouts!\n"
	exit 1
fi

array_index () {
	local -n array=$1
	string=$2
	for i in "${!array[@]}"; do
		if [[ "${array[$i]}" = "$string" ]]; then
			return $i
		fi
	done
	return -1
}

check_status () {
	index=0

	# Iterate through detected packages
	# and build out arrays of devices, statuses and Git repos
	while read line; do
		IFS='|' read -r -a package <<< "$line"
		package_name=${package[0]}
		package_library=${package[1]}
		package_status=${package[2]}
		DEVICES[$index]=$package_name
		STATUSES[$index]=$package_status
		REPOS[$index]=$package_library
		index=$(($index+1))
	done < <(echo -e "$DETECTED")
}

do_uninstall () {
	index=$1
	package_name=${DEVICES[$index]}
	package_library=${REPOS[$index]}

	git_dir=$package_library
	cd $TMP_DIR
	if [[ ! -d "$git_dir/.git" ]]; then
		if [[ ! "$VERBOSE" = "" ]]; then
			rm -f $git_dir > $LOG_FILE
			git clone https://github.com/pimoroni/$package_library $git_dir
		else
			rm -f $git_dir > $LOG_FILE 2>&1
			git clone https://github.com/pimoroni/$package_library $git_dir > $LOG_FILE 2>&1
		fi
	fi
	cd $git_dir
	git pull origin master > $LOG_FILE 2>&1
	if [[ -f "uninstall.sh" ]]; then
		if [[ ! "$VERBOSE" == "" ]]; then
			./uninstall.sh
		else
			./uninstall.sh > $LOG_FILE 2>&1
		fi
	else
		if [[ ! "$VERBOSE" == "" ]]; then
			echo "Warning: No uninstall.sh found for $package_name."
		else
			echo "Warning: No uninstall.sh found for $package_name." > $LOG_FILE 2>&1
		fi
		STATUSES[$index]="error"
		return 1
	fi
	cd $TMP_DIR
	rm -r $git_dir
	cd $WORKING_DIR
	STATUSES[$index]="uninstalled"
}

do_install () {
	index=$1
	package_name=${DEVICES[$index]}
	package_library=${REPOS[$index]}

	git_dir=$package_library
	cd $TMP_DIR
	if [[ ! -d "$git_dir/.git" ]]; then
		if [[ ! "$VERBOSE" == "" ]]; then
			rm -f $git_dir > $LOG_FILE
			git clone https://github.com/pimoroni/$package_library $git_dir
		else
			rm -f $git_dir > $LOG_FILE 2>&1
			git clone https://github.com/pimoroni/$package_library $git_dir > $LOG_FILE 2>&1
		fi
	fi
	cd $git_dir
	git pull origin master > $LOG_FILE 2>&1
	if [[ -f "install.sh" ]]; then
		if [[ ! "$VERBOSE" == "" ]]; then
			"./install.sh"
		else
			"./install.sh" > $LOG_FILE 2>&1
		fi
	else
		echo "Warning: No install.sh found for $package_name." > $LOG_FILE 2>&1
		STATUSES[$index]="noinstall"
		return 1
	fi
	cd $WORKING_DIR

	STATUSES[$index]="installed"
}

warn_if () {
	for ((y = 0; y < $COUNT; y++)); do
		STATUS=${STATUSES[$y]}
		if [[ "$STATUS" == "$1" ]]; then
			warning "$2"
			printf "\n"
			break;
		fi
	done
}

display () {
	if [[ "$VERBOSE" == "" ]]; then
		lines=$(tput lines)
		lines=$(($lines-$COUNT-$PADDING))
		tput cup $lines 0
	fi
	for ((i = 0; i < $COUNT; i++)); do
		ITEM=${DEVICES[$i]}
		STATUS=${STATUSES[$i]}

		if [[ "$VERBOSE" == "" ]] || [[ "" == "$1" ]] || [[ "$i" == "$1" ]]; then
			printf "%-30s %s" "$ITEM:" " "
			case $STATUS in
				"error"*)
					warning "Error!         ";;
				"noinstall"*)
					warning "Unsupported!   ";;
				"required"*)
					warning "Required       ";;
				"installed"*)
					success "Installed      ";;
				"uninstalled"*)
					success "Uninstalled    ";;
				"uninstalling"*)
					inform  "Uninstalling...";;
				"installing"*)
					inform  "Installing...  ";;
				"reinstalling"*)
					inform  "Reinstalling...";;
			esac
			printf "\n"
		fi
	done
}

check_status

installs_required=0
uninstalls_required=0

printf "\n"

printf "Breakout Garden: Installer.\n"
printf "Found $COUNT breakout(s):\n\n"

for ((y = 0; y < $COUNT; y++)); do
	if [[ "$VERBOSE" == "" ]]; then
		printf "\n"
	fi
	if [[ "${STATUSES[$y]}" == "required" ]] || [[ ! "$FORCE" == "" ]]; then
		installs_required=$(($installs_required+1))
	fi
	if [[ "$ACTION" == "uninstall" ]] && [[ "${STATUSES[$y]}" == "installed" ]]; then
		uninstalls_required=$(($uninstalls_required+1))
	fi
done

if [[ "$VERBOSE" == "" ]]; then
	printf "\n\n\n\n"
fi

display

printf "\n"

if [[ "$ACTION" == "install" ]]; then
	if [[ "$installs_required" == "0" ]]; then
		read -p "Nothing to do! Press enter to quit..."
	else
		action_text="Installing"
		if [[ ! "$FORCE" == "" ]]; then
			forced_mode=" (forced)"
			action_text="Reinstalling"
		fi
		read -p "$action_text $installs_required module(s)$forced_mode. Enter to continue (Ctrl+C to cancel)..."

		for ((y = 0; y < $COUNT; y++)); do
			STATUS=${STATUSES[$y]}
			if [[ ! "$STATUS" == "installed" ]] || [[ ! "$FORCE" == "" ]]; then
				if [[ ! "$FORCE" == "" ]]; then
					STATUSES[$y]="reinstalling"
				else
					STATUSES[$y]="installing"
				fi

				display $y

				do_install $y
				display $y
			fi
		done
	fi
fi

if [[ "$ACTION" == "uninstall" ]]; then
	if [[ "$uninstalls_required" == "0" ]]; then
		read -p "Nothing to do! Press enter to quit..."
	else
		read -p "Removing $uninstalls_required module(s). Enter to continue (Ctrl+C to cancel)..."

		for ((y = 0; y < $COUNT; y++)); do
			STATUS=${STATUSES[$y]}
			if [[ "$STATUS" == "installed" ]]; then
				STATUSES[$y]="uninstalling"
				display $y

				do_uninstall $y
				display $y
			fi
		done

	fi
fi

printf "\n\n"

warn_if "error" "Errors occured during $ACTION. For more info see $LOG_FILE"
warn_if "noinstall" "\nOne or more libraries don't support auto installation:"

for ((y = 0; y < $COUNT; y++)); do
	STATUS=${STATUSES[$y]}
	package_name=${DEVICES[$y]}
	package_library=${REPOS[$y]}

	if [[ "$STATUS" == "noinstall" ]]; then
		printf "%-30s %s" "$package_name:" " "
		printf "See: https://github.com/pimoroni/$package_library\n"
	fi
done

