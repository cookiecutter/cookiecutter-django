#!/usr/bin/env bash

### Remove a database backup.
###
### Parameters:
###     <1> filename of a backup to remove.
###
### Usage:
###     $ docker-compose -f <environment>.yml (exec |run --rm) postgres rmbackup <1>


set -o errexit
set -o pipefail
set -o nounset


working_dir="$(dirname ${0})"
source "${working_dir}/_sourced/constants.sh"
source "${working_dir}/_sourced/messages.sh"


if [[ -z ${1+x} ]]; then
    message_error "Backup filename is not specified yet it is a required parameter. Make sure you provide one and try again."
    exit 1
fi
backup_filename="${BACKUP_DIR_PATH}/${1}"
if [[ ! -f "${backup_filename}" ]]; then
    message_error "No backup with the specified filename found. Check out the 'backups' maintenance script output to see if there is one and try again."
    exit 1
fi

message_welcome "Removing the '${backup_filename}' backup file..."

rm -r "${backup_filename}"

message_success "The '${backup_filename}' database backup has been removed."
