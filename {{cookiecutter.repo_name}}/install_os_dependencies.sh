#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo -e "\nYou must run this with root privilege" 2>&1
    echo -e "Please do:\n" 2>&1
    echo "sudo ./${0##*/}" 2>&1
    echo -e "\n" 2>&1

    exit 1
else

    apt-get update

    # Install the basic compilation dependencies and other required libraries of this project
    cat requirements.apt | grep -v "#" | xargs sudo apt-get install -y

    # cleaning downloaded packages from apt-get cache
    apt-get clean

fi
