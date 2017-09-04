#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


echo "listing available backups"
echo "-------------------------"
ls /backups/
