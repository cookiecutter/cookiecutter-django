from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import tomllib

ROOT = Path(__file__).parent.parent
TEMPLATED_ROOT = ROOT / "{{cookiecutter.project_slug}}"
REQUIREMENTS_LOCAL_TXT = TEMPLATED_ROOT / "requirements" / "local.txt"
TEMPLATE_PRE_COMMIT_CONFIG = ROOT / ".pre-commit-config.yaml"
PRE_COMMIT_CONFIG = TEMPLATED_ROOT / ".pre-commit-config.yaml"
PYPROJECT_TOML = ROOT / "pyproject.toml"

PRE_COMMIT_REPOS = {
    "ruff": "https://github.com/astral-sh/ruff-pre-commit",
    "djlint": "https://github.com/djlint/djLint",
}


def main(package_name: str) -> None:
    new_version = get_requirements_txt_version(package_name)
    old_version = get_pyproject_toml_version(package_name)
    if old_version == new_version:
        return

    update_package_version(package_name, old_version, new_version)
    subprocess.run(["uv", "lock", "--no-upgrade"], cwd=ROOT, check=False)  # noqa: S607


def get_requirements_txt_version(package_name: str) -> str:
    content = REQUIREMENTS_LOCAL_TXT.read_text()
    for line in content.split("\n"):
        if line.startswith(package_name):
            return line.split(" ")[0].split("==")[1]
    msg = f"Could not find {package_name} version in requirements/local.txt"
    raise RuntimeError(msg)


def get_pyproject_toml_version(package_name: str) -> str:
    data = tomllib.loads(PYPROJECT_TOML.read_text())
    for dependency in data["project"]["dependencies"]:
        if dependency.startswith(f"{package_name}=="):
            return dependency.split("==")[1]
    msg = f"Could not find {package_name} version in pyproject.toml"
    raise RuntimeError(msg)


def update_package_version(package_name: str, old_version: str, new_version: str) -> None:
    # Update pyproject.toml
    new_content = PYPROJECT_TOML.read_text().replace(
        f"{package_name}=={old_version}",
        f"{package_name}=={new_version}",
    )
    PYPROJECT_TOML.write_text(new_content)
    # Update pre-commit configs
    repo_url = PRE_COMMIT_REPOS[package_name]
    for config_file in [PRE_COMMIT_CONFIG, TEMPLATE_PRE_COMMIT_CONFIG]:
        new_content = config_file.read_text().replace(
            f"repo: {repo_url}\n    rev: v{old_version}",
            f"repo: {repo_url}\n    rev: v{new_version}",
        )
        config_file.write_text(new_content)


if __name__ == "__main__":
    if len(sys.argv) < 2:  # noqa: PLR2004
        print("Usage: python3 python_dependency_version.py <dependency name>")
        sys.exit(1)
    dep_name = sys.argv[1]
    main(dep_name)
