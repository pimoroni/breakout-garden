#!/bin/bash

if [ $(id -u) -ne 0 ]; then
	printf "Breakout Garden: Installer\n\n"
	printf "Script must be run as root. Try 'sudo ./install.sh'\n"
	exit 1
fi

success() {
	printf "$(tput setaf 2)$1$(tput setaf 7)"
}

inform() {
	printf "$(tput setaf 6)$1$(tput setaf 7)"
}

warning() {
	printf "$(tput setaf 1)$1$(tput setaf 7)"
}

WORKING_DIR=`pwd`
TMP_DIR="/tmp/breakout-garden"
LOG_FILE="$TMP_DIR/install.log"


DEVICES=()
STATUSES=()
REPOS=()

PADDING=5

DETECTED=`python autodetect.py --install`

COUNT=`echo -e "$DETECTED" | wc -l`

if [[ "$COUNT" -eq "0" ]] || [[ "$DETECTED" == "" ]]; then
	printf "Sorry, I couldn't find any breakouts!\n"
	exit 1
fi

if [[ -f "/usr/bin/python3" ]]; then
	DETECTED3=`python3 autodetect.py --install`
fi

array_index () {
	local -n array=$1
	string=$2
	printf "$array $string\n"
	for i in "${!array[@]}"; do
		if [[ "${array[$i]}" = "$string" ]]; then
			return $i
		fi
	done
	return -1
}

check_status () {
	index=0

	# Iterate through Python3 detected packages
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

	# Iterate through Python3 detected packages
	# and update status to required if they are missing
	if [[ ! "$DETECTED3" = "" ]]; then
		while read line; do
			IFS='|' read -r -a package <<< "$line"
			package_name=${package[0]}
			package_library=${package[1]}
			package_status=${package[2]}

			# Find the index of the package in our original array
			# that we produced in the first loop above
			array_index DEVICES "$package_name"
			index=$?

			if [[ ! "$index" == "-1" ]] && [[ "$package_status" == "required" ]]; then
				STATUSES[$index]=$package_status
			fi
		done < <(echo -e "$DETECTED3")
	fi
}

do_install () {
	index=$1
	package_name=${DEVICES[$index]}
	package_library=${REPOS[$index]}

	git_dir=$package_library
	cd $TMP_DIR
	if [[ ! -d "$git_dir/.git" ]]; then
		rm -f $git_dir > $LOG_FILE 2>&1
		git clone https://github.com/pimoroni/$package_library $git_dir > $LOG_FILE 2>&1
	fi
	cd $git_dir
	git pull origin master > $LOG_FILE 2>&1
	if [[ -f "install.sh" ]]; then
		./install.sh > $LOG_FILE 2>&1
	else
		echo "Warning: No install.sh found for $line."  $LOG_FILE 2>&1
		STATUSES[$index]="error"
		return 1
	fi
	cd $WORKING_DIR

	STATUSES[$index]="installed"
}

display () {
	lines=$(tput lines)
	lines=$(($lines-$COUNT-$PADDING))
	tput cup $lines 0
	printf "Breakout Garden: Installer. ($COUNT breakout(s) found) \n\n"
	for ((i = 0; i < $COUNT; i++)); do
		ITEM=${DEVICES[$i]}
		STATUS=${STATUSES[$i]}
		status_text=""
		printf "%-30s %s" "$ITEM:" " "
		case $STATUS in
			"error"*)
				warning "Error!       ";;
			"required"*)
				warning "Required     ";;
			"installed"*)
				success "Installed    ";;
			"installing"*)
				inform  "Installing...";;
		esac
		printf "\n"
	done
	printf "\n"
}

check_status

installs_required=0

for ((y = 0; y < $COUNT; y++)); do
	printf "\n"
	if [[ "${STATUSES[$y]}" = "required" ]]; then
		installs_required=$(($installs_required+1))
	fi
done

printf "\n\n\n\n\n"

display

if [[ "$installs_required" = "0" ]]; then
	read -p "Nothing to do! Press enter to quit..."
else
	read -p "$installs_required required. Press enter to continue (Ctl+C to cancel)..."

	for ((y = 0; y < $COUNT; y++)); do
		STATUS=${STATUSES[$y]}
		if [[ ! "$STATUS" == "installed" ]]; then
			STATUSES[$y]="installing"
			display

			do_install $y
			display
		fi
	done
fi

printf "\n\n"
