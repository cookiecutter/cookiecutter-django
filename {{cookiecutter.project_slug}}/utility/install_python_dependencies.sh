#!/bin/bash

WORK_DIR="$(dirname "$0")"
PROJECT_DIR="$(dirname "$WORK_DIR")"

uv --version >/dev/null 2>&1 || {
    echo >&2 -e "\nuv is required but it's not installed."
    echo >&2 -e "You can install it by following the instructions at https://github.com/astral-sh/uv#installation"
    exit 1;
}

uv sync --locked
