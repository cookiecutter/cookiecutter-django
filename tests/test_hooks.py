"""Unit tests for the hooks"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from jinja2 import Environment
from jinja2 import StrictUndefined

from hooks.post_gen_project import append_to_gitignore_file


@pytest.fixture
def working_directory(tmp_path):
    prev_cwd = Path.cwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(prev_cwd)


def test_append_to_gitignore_file(working_directory):
    gitignore_file = working_directory / ".gitignore"
    gitignore_file.write_text("node_modules/\n")
    append_to_gitignore_file(".envs/*")
    linesep = os.linesep.encode()
    assert gitignore_file.read_bytes() == b"node_modules/" + linesep + b".envs/*" + linesep
    assert gitignore_file.read_text() == "node_modules/\n.envs/*\n"


@pytest.mark.parametrize(
    ("project_slug", "rest_api", "exit_code"),
    [
        ("ninja", "Django Ninja", 1),
        ("ninja_app", "Django Ninja", 0),
        ("ninja", "None", 0),
        ("ninja", "DRF", 0),
    ],
)
def test_ninja_project_slug(tmp_path, project_slug, rest_api, exit_code):
    root = Path(__file__).resolve().parent.parent
    context = json.loads((root / "cookiecutter.json").read_text())
    context = {name: value[0] if isinstance(value, list) else value for name, value in context.items()}
    context.update(project_slug=project_slug, rest_api=rest_api)
    environment = Environment(undefined=StrictUndefined, autoescape=False)  # noqa: S701
    template = environment.from_string((root / "hooks/pre_gen_project.py").read_text())
    hook = tmp_path / "pre_gen_project.py"
    hook.write_text(template.render(cookiecutter=context))

    result = subprocess.run(  # noqa: S603
        [sys.executable, str(hook)],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
    )

    assert result.returncode == exit_code, result.stdout + result.stderr
    if exit_code:
        assert "conflicts with Django Ninja" in result.stdout
        assert "ninja_app" in result.stdout
