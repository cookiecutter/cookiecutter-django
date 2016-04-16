#!/bin/bash

## Verify that we are running this script on Centos or Ubuntu
command -v lsb_release >/dev/null 2>&1 || { echo >&2 "This setup script only currently works on Centos and Ubuntu. Aborting."; exit 1; }

## Get the Distribution type from lsb_release
OS=$(lsb_release -si)
case "$OS" in
    CentOS) OS_REQUIREMENTS_FILENAME="requirements.yum";;
    Ubuntu) OS_REQUIREMENTS_FILENAME="requirements.apt";;
esac

# Handle call with wrong command
function wrong_command()
{
  echo "${0##*/} - unknown command: '${1}'"
  usage_message
}

# Print help / script usage
function usage_message()
{
  echo "usage: ./${0##*/} <command>"
  echo "available commands are:"
  echo -e "\tlist\t\tPrint a list of all packages defined on ${OS_REQUIREMENTS_FILENAME} file"
  echo -e "\thelp\t\tPrint this help"
  echo -e "\n\tCommands that require superuser permission:"
  echo -e "\tinstall\t\tInstall packages defined on ${OS_REQUIREMENTS_FILENAME} file. Note: This\n\t\t\t   does not upgrade the packages already installed for new\n\t\t\t   versions, even if new version is available in the repository."
  echo -e "\tupgrade\t\tSame that install, but upgrate the already installed packages,\n\t\t\t   if new version is available."

}

# Read the requirements.apt file, and remove comments and blank lines
function list_packages(){
     grep -v "#" ${OS_REQUIREMENTS_FILENAME} | grep -v "^$";
}

function install()
{
    case "$OS" in 
        CentOS) list_packages | xargs yum install -y;;
        Ubuntu) list_packages | xargs apt-get --no-upgrade install -y;;
    esac
}

function upgrade()
{
    case "$OS" in 
        CentOS) list_packages | xargs yum install -y;;
        Ubuntu) list_packages | xargs apt-get install -y;;
    esac
}


function install_or_upgrade()
{
    P=${1}
    PARAN=${P:-"install"}

    if [[ $EUID -ne 0 ]]; then
        echo -e "\nYou must run this with root privilege" 2>&1
        echo -e "Please do:\n" 2>&1
        echo "sudo ./${0##*/} $PARAN" 2>&1
        echo -e "\n" 2>&1

        exit 1
    else
        case "$OS" in
            CentOS) yum update;;
            Ubuntu) apt-get clean;;
        esac

        # Install the basic compilation dependencies and other required libraries of this project
        if [ "$PARAN" == "install" ]; then
            install;
        else
            upgrade;
        fi

        # cleaning downloaded packages from apt-get cache
        case "$OS" in
            CentOS) yum clean all;;
            Ubuntu) apt-get clean;;
        esac
        exit 0
    fi


}

# Handle command argument
case "$1" in
    install) install_or_upgrade;;
    upgrade) install_or_upgrade "upgrade";;
    list) list_packages;;
    help) usage_message;;
    *) wrong_command $1;;
esac
