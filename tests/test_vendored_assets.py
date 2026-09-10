"""Integrity checks for third-party assets vendored into the template."""

import hashlib
import json
from pathlib import Path

TEMPLATE_ROOT = Path(__file__).parent.parent / "{{cookiecutter.project_slug}}" / "{{cookiecutter.project_slug}}"
PICO_DIR = TEMPLATE_ROOT / "static" / "vendor" / "pico"


def test_pico_metadata_matches_vendored_file():
    metadata = json.loads((PICO_DIR / "pico.json").read_text())
    css = (PICO_DIR / metadata["file"]).read_bytes()

    assert metadata["license"] == "MIT"
    assert hashlib.sha256(css).hexdigest() == metadata["sha256"]
    assert f"v{metadata['version']}".encode() in css[:300]
    assert (PICO_DIR / "LICENSE.md").read_text().startswith("MIT License")
