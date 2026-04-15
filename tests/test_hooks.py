"""Unit tests for the hooks"""

import os
from pathlib import Path

import pytest

from hooks.post_gen_project import append_to_gitignore_file
from hooks.post_gen_project import remove_open_source_files
from hooks.post_gen_project import remove_gplv3_files


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


def test_bug1_jinja_variable_spacing():
    with open("hooks/post_gen_project.py", encoding="utf-8") as f:
        content = f.read()
    assert "cookiecutter.open_source_license}}" not in content
    assert "cookiecutter.cloud_provider}}" not in content
    assert "cookiecutter.open_source_license }}" in content
    assert "cookiecutter.cloud_provider }}" in content


def test_bug2_namedtuple_no_len_check():
    with open("scripts/create_django_issue.py", encoding="utf-8") as f:
        content = f.read()
    assert "len(version) == 2:" not in content


def test_bug3_file_deletion_with_missing_ok(working_directory):
    remove_open_source_files()
    Path("CONTRIBUTORS.txt").write_text("test")
    remove_open_source_files()
    assert not Path("CONTRIBUTORS.txt").exists()
    remove_gplv3_files()
    assert True


def test_bug4_case_insensitive_comparison():
    with open("hooks/post_gen_project.py", encoding="utf-8") as f:
        content = f.read()
    assert '"{{ cookiecutter.cloud_provider }}" != "AWS"' not in content
    assert '"{{ cookiecutter.cloud_provider }}".lower() != "aws"' in content
    assert '"{{ cookiecutter.cloud_provider }}" == "None"' not in content
    assert '"{{ cookiecutter.cloud_provider }}".lower() == "none"' in content
    assert '"{{ cookiecutter.editor }}" == "PyCharm"' not in content
    assert '"{{ cookiecutter.editor }}".lower() == "pycharm"' in content
    assert '"{{ cookiecutter.editor }}" != "PyCharm"' not in content
    assert '"{{ cookiecutter.editor }}".lower() != "pycharm"' in content
    assert 'choice == "Gulp"' not in content
    assert 'choice.lower() == "gulp"' in content
    assert 'choice == "Webpack"' not in content
    assert 'choice.lower() == "webpack"' in content
    assert '"{{ cookiecutter.open_source_license }}" == "Not open source"' not in content
    assert '"{{ cookiecutter.open_source_license }}".lower() == "not open source"' in content
    assert '"{{ cookiecutter.open_source_license }}" != "GPLv3"' not in content
    assert '"{{ cookiecutter.open_source_license }}".lower() != "gplv3"' in content
    assert '"{{ cookiecutter.username_type }}" == "username"' not in content
    assert '"{{ cookiecutter.username_type }}".lower() == "username"' in content
    assert 'in ["None", "Django Compressor"]' not in content
    assert 'in ["none", "django compressor"]' in content
    assert '"{{ cookiecutter.rest_api }}" == "DRF"' not in content
    assert '"{{ cookiecutter.rest_api }}".lower() == "drf"' in content
    assert '"{{ cookiecutter.rest_api }}" == "Django Ninja"' not in content
    assert '"{{ cookiecutter.rest_api }}".lower() == "django ninja"' in content
    assert '"{{ cookiecutter.ci_tool }}" != "Travis"' not in content
    assert '"{{ cookiecutter.ci_tool }}".lower() != "travis"' in content
    assert '"{{ cookiecutter.ci_tool }}" != "Gitlab"' not in content
    assert '"{{ cookiecutter.ci_tool }}".lower() != "gitlab"' in content
    assert '"{{ cookiecutter.ci_tool }}" != "Github"' not in content
    assert '"{{ cookiecutter.ci_tool }}".lower() != "github"' in content
    assert '"{{ cookiecutter.ci_tool }}" != "Drone"' not in content
    assert '"{{ cookiecutter.ci_tool }}".lower() != "drone"' in content


def test_bug5_no_dead_code_in_heroku_files():
    with open("hooks/post_gen_project.py", encoding="utf-8") as f:
        content = f.read()
    assert 'file_names = ["Procfile", "requirements.txt"]' in content
    assert 'file_names = ["Procfile"]' not in content


def test_bug6_no_broad_exception_catch():
    with open("hooks/post_gen_project.py", encoding="utf-8") as f:
        content = f.read()
    assert "except Exception as e" not in content
    assert "except OSError as e" in content

