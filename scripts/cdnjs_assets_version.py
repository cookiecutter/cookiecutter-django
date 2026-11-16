"""
Keep CDNjs-hosted assets in the HTML templates in line with package.json.

When the frontend pipeline is "None", the generated project loads some
libraries (e.g. Bootstrap) from cdnjs.cloudflare.com instead of npm. This
script reads the version installed via npm and updates the CDN URLs and their
Subresource Integrity (SRI) hashes accordingly.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent
TEMPLATED_ROOT = ROOT / "{{cookiecutter.project_slug}}"
PACKAGE_LOCK_JSON = TEMPLATED_ROOT / "package-lock.json"
HTML_TEMPLATES = [
    TEMPLATED_ROOT / "{{cookiecutter.project_slug}}" / "templates" / "base.html",
]
CDNJS_BASE_URL = "https://cdnjs.cloudflare.com/ajax/libs"

# npm package name -> cdnjs library name
CDNJS_LIBRARIES = {
    "bootstrap": "bootstrap",
}


def main() -> None:
    changed = False
    for package_name, cdnjs_name in CDNJS_LIBRARIES.items():
        version = get_package_lock_version(package_name)
        for template in HTML_TEMPLATES:
            changed |= update_template(template, cdnjs_name, version)
    if not changed:
        print("All CDNjs assets are up to date.")


def get_package_lock_version(package_name: str) -> str:
    data = json.loads(PACKAGE_LOCK_JSON.read_text())
    try:
        return data["packages"][f"node_modules/{package_name}"]["version"]
    except KeyError:
        msg = f"Could not find {package_name} version in package-lock.json"
        raise RuntimeError(msg) from None


def update_template(template: Path, cdnjs_name: str, new_version: str) -> bool:
    """Update URLs + integrity attributes for one library. Return True if changed."""
    # Matches a cdnjs URL for the library, followed by its integrity attribute
    pattern = re.compile(
        rf'(?P<prefix>"{re.escape(CDNJS_BASE_URL)}/{re.escape(cdnjs_name)}/)'
        r"(?P<version>[^/\"]+)"
        r'(?P<path>/[^"]+)"'
        r'(?P<between>\s+integrity=")'
        r'(?P<integrity>[^"]+)"',
    )
    content = template.read_text()

    def replace(match: re.Match[str]) -> str:
        if match["version"] == new_version:
            return match[0]
        url = f"{CDNJS_BASE_URL}/{cdnjs_name}/{new_version}{match['path']}"
        integrity = compute_sri_hash(url)
        print(f"{template.relative_to(ROOT)}: {cdnjs_name} {match['version']} -> {new_version} ({match['path']})")
        return f'{match["prefix"]}{new_version}{match["path"]}"{match["between"]}{integrity}"'

    new_content, count = pattern.subn(replace, content)
    if count == 0:
        msg = f"Could not find any {cdnjs_name} CDNjs asset in {template.relative_to(ROOT)}"
        raise RuntimeError(msg)
    if new_content == content:
        return False
    template.write_text(new_content)
    return True


def compute_sri_hash(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    digest = hashlib.sha512(response.content).digest()
    return f"sha512-{base64.b64encode(digest).decode()}"


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
