#!/bin/bash

set -e

echo "Installing dependencies using uv..."

{% if cookiecutter.use_docker == "y" %}
docker compose -f docker-compose.local.yml build django
uv="docker compose -f docker-compose.local.yml run --rm django uv"
{% else %}
uv="uv"
{% endif %}

$uv add -r requirements/production.txt
$uv add --dev -r requirements/local.txt

rm -rf requirements

echo "Setup complete!"
