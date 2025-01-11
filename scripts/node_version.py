import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEMPLATED_ROOT = ROOT / "{{cookiecutter.project_slug}}"
DOCKERFILE = TEMPLATED_ROOT / "compose" / "local" / "node" / "Dockerfile"
PACKAGE_JSON = TEMPLATED_ROOT / "package.json"
CI_YML = ROOT / ".github" / "workflows" / "ci.yml"


class VersionNotFoundError(RuntimeError):
    def __init__(self):
        super().__init__("Could not find version in Dockerfile")


def main():
    new_version = get_version_from_dockerfile()
    old_version = get_version_from_package_json()
    if old_version != new_version:
        update_package_json_version(old_version, new_version)
        update_ci_node_version(old_version, new_version)


def get_version_from_dockerfile():
    # Extract version out of base image name:
    # FROM docker.io/node:22.13-bookworm-slim
    # -> 22.13
    with DOCKERFILE.open("r") as f:
        for line in f:
            if "FROM docker.io/node:" in line:
                _, _, docker_tag = line.partition(":")
                version_str, _, _ = docker_tag.partition("-")
                return version_str
    raise VersionNotFoundError


def get_version_from_package_json():
    package_json = json.loads(PACKAGE_JSON.read_text())
    return package_json["engines"]["node"]


def update_package_json_version(old_version, new_version):
    package_json_text = PACKAGE_JSON.read_text()
    package_json_text = package_json_text.replace(
        f'"node": "{old_version}"',
        f'"node": "{new_version}"',
    )
    PACKAGE_JSON.write_text(package_json_text)


def update_ci_node_version(old_version, new_version):
    yml_content = CI_YML.read_text()
    yml_content = yml_content.replace(
        f'node-version: "{old_version}"',
        f'node-version: "{new_version}"',
    )
    CI_YML.write_text(yml_content)


if __name__ == "__main__":
    main()
