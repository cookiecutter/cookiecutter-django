#!/bin/bash

WORK_DIR="$(dirname "$0")"
DISTRO_NAME=$(lsb_release -sc)
OS_REQUIREMENTS_FILENAME="requirements-$DISTRO_NAME.apt"

cd $WORK_DIR

# Check if a requirements file exist for the current distribution.
if [ ! -r "$OS_REQUIREMENTS_FILENAME" ]; then
    cat <<-EOF >&2
		There is no requirements file for your distribution.
		You can see one of the files listed below to help search the equivalent package in your system:
		$(find ./ -name "requirements-*.apt" -printf "  - %f\n")
	EOF
    exit 1;
fi

# Handle call with wrong command
function wrong_command()
{
    echo "${0##*/} - unknown command: '${1}'" >&2
    usage_message
}

# Print help / script usage
function usage_message()
{
    cat <<-EOF
		Usage: $WORK_DIR/${0##*/} <command>
		Available commands are:
		    list        Print a list of all packages defined on ${OS_REQUIREMENTS_FILENAME} file
		    help        Print this help

		Commands that require superuser permission:
		    install     Install packages defined on ${OS_REQUIREMENTS_FILENAME} file. Note: This
		                does not upgrade the packages already installed for new versions, even if
		                new version is available in the repository.
		    upgrade     Same that install, but upgrade the already installed packages, if new
		                version is available.
	EOF
}

# Read the requirements.apt file, and remove comments and blank lines
function list_packages(){
    grep -v "#" "${OS_REQUIREMENTS_FILENAME}" | grep -v "^$";
}

function install_packages()
{
    list_packages | xargs apt-get --no-upgrade install -y;
}

function upgrade_packages()
{
    list_packages | xargs apt-get install -y;
}

function install_or_upgrade()
{
    P=${1}
    PARAN=${P:-"install"}

    if [[ $EUID -ne 0 ]]; then
        cat <<-EOF >&2
			You must run this script with root privilege
			Please do:
			sudo $WORK_DIR/${0##*/} $PARAN
		EOF
        exit 1
    else

        apt-get update

        # Install the basic compilation dependencies and other required libraries of this project
        if [ "$PARAN" == "install" ]; then
            install_packages;
        else
            upgrade_packages;
        fi

        # cleaning downloaded packages from apt-get cache
        apt-get clean

        exit 0
    fi
}

# Handle command argument
case "$1" in
    install) install_or_upgrade;;
    upgrade) install_or_upgrade "upgrade";;
    list) list_packages;;
    help|"") usage_message;;
    *) wrong_command "$1";;
esac
