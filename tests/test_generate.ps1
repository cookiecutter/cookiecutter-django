# this is a very simple script that tests the generation for cookiecutter-django with Windows
# it is meant to be run from the root directory of the repository, eg: powershell tests/test_generate.ps1

$ErrorActionPreference = "Stop"
Set-PSDebug -Trace 1

# create a cache directory
New-Item -ItemType Directory -Force -Path .cache/bare | Out-Null
Set-Location .cache/bare

# create the project using the default settings in cookiecutter.json
Invoke-Expression "uv run cookiecutter ../../ --no-input --overwrite-if-exists use_docker=n $env:COOKIECUTTER_ARGS"
Set-Location my_awesome_project

# Install Python deps
# uv sync
