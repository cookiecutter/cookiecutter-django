"""Unit tests for the hooks"""

import os
import shutil
from pathlib import Path

import pytest

from hooks.post_gen_project import (
    append_to_gitignore_file,
    remove_aws_dockerfile,
    remove_celery_compose_dirs,
    remove_celery_files,
    remove_custom_user_manager_files,
    remove_docker_files,
    remove_dotdrone_file,
    remove_dotgithub_folder,
    remove_dotgitlabciyml_file,
    remove_dottravisyml_file,
    remove_drf_starter_files,
    remove_envs_and_associated_files,
    remove_gplv3_files,
    remove_gulp_files,
    remove_heroku_files,
    remove_nginx_docker_files,
    remove_ninja_starter_files,
    remove_node_dockerfile,
    remove_open_source_files,
    remove_packagejson_file,
    remove_rest_api_files,
    remove_sass_files,
    remove_utility_files,
    remove_webpack_files,
)


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


class TestBug3FileDeletionExistenceCheck:
    """Test cases for Bug 3: File/directory deletion without existence check"""

    def test_remove_open_source_files_missing_files(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_open_source_files()

    def test_remove_open_source_files_existing_files(self, working_directory):
        """Should remove files when they exist"""
        (working_directory / "CONTRIBUTORS.txt").write_text("test")
        (working_directory / "LICENSE").write_text("test")
        remove_open_source_files()
        assert not (working_directory / "CONTRIBUTORS.txt").exists()
        assert not (working_directory / "LICENSE").exists()

    def test_remove_gplv3_files_missing_files(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_gplv3_files()

    def test_remove_gplv3_files_existing_files(self, working_directory):
        """Should remove files when they exist"""
        (working_directory / "COPYING").write_text("test")
        remove_gplv3_files()
        assert not (working_directory / "COPYING").exists()

    def test_remove_custom_user_manager_files_missing(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_custom_user_manager_files()

    def test_remove_docker_files_missing(self, working_directory):
        """Should not raise error when directories don't exist"""
        remove_docker_files()

    def test_remove_docker_files_existing(self, working_directory):
        """Should remove directories when they exist"""
        (working_directory / ".devcontainer").mkdir()
        (working_directory / "compose").mkdir()
        (working_directory / "docker-compose.local.yml").write_text("test")
        remove_docker_files()
        assert not (working_directory / ".devcontainer").exists()
        assert not (working_directory / "compose").exists()
        assert not (working_directory / "docker-compose.local.yml").exists()

    def test_remove_nginx_docker_files_missing(self, working_directory):
        """Should not raise error when directory doesn't exist"""
        remove_nginx_docker_files()

    def test_remove_utility_files_missing(self, working_directory):
        """Should not raise error when directory doesn't exist"""
        remove_utility_files()

    def test_remove_heroku_files_missing(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_heroku_files()

    def test_remove_heroku_files_existing(self, working_directory):
        """Should remove files when they exist"""
        (working_directory / "Procfile").write_text("test")
        (working_directory / "bin").mkdir()
        remove_heroku_files()
        assert not (working_directory / "Procfile").exists()
        assert not (working_directory / "bin").exists()

    def test_remove_sass_files_missing(self, working_directory):
        """Should not raise error when directory doesn't exist"""
        remove_sass_files()

    def test_remove_gulp_files_missing(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_gulp_files()

    def test_remove_webpack_files_missing(self, working_directory):
        """Should not raise error when directory doesn't exist"""
        remove_webpack_files()

    def test_remove_packagejson_file_missing(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_packagejson_file()

    def test_remove_celery_files_missing(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_celery_files()

    def test_remove_dottravisyml_file_missing(self, working_directory):
        """Should not raise error when file doesn't exist"""
        remove_dottravisyml_file()

    def test_remove_dotgitlabciyml_file_missing(self, working_directory):
        """Should not raise error when file doesn't exist"""
        remove_dotgitlabciyml_file()

    def test_remove_dotgithub_folder_missing(self, working_directory):
        """Should not raise error when directory doesn't exist"""
        remove_dotgithub_folder()

    def test_remove_dotdrone_file_missing(self, working_directory):
        """Should not raise error when file doesn't exist"""
        remove_dotdrone_file()

    def test_remove_envs_and_associated_files_missing(self, working_directory):
        """Should not raise error when directories don't exist"""
        remove_envs_and_associated_files()

    def test_remove_celery_compose_dirs_missing(self, working_directory):
        """Should not raise error when directories don't exist"""
        remove_celery_compose_dirs()

    def test_remove_node_dockerfile_missing(self, working_directory):
        """Should not raise error when directory doesn't exist"""
        remove_node_dockerfile()

    def test_remove_aws_dockerfile_missing(self, working_directory):
        """Should not raise error when directory doesn't exist"""
        remove_aws_dockerfile()

    def test_remove_drf_starter_files_missing(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_drf_starter_files()

    def test_remove_ninja_starter_files_missing(self, working_directory):
        """Should not raise error when files don't exist"""
        remove_ninja_starter_files()

    def test_remove_rest_api_files_missing(self, working_directory):
        """Should not raise error when directories don't exist"""
        remove_rest_api_files()


class TestBug1JinjaTemplateVariableSpacing:
    """Test cases for Bug 1: Jinja template variable name spacing error"""

    def test_open_source_license_variable_spacing(self):
        """Verify open_source_license variable has correct spacing in hooks"""
        from hooks import post_gen_project

        source = open(post_gen_project.__file__, encoding="utf-8").read()
        assert '{{ cookiecutter.open_source_license }}"' in source
        assert '{{ cookiecutter.open_source_license}}"' not in source

    def test_cloud_provider_variable_spacing(self):
        """Verify cloud_provider variable has correct spacing in hooks"""
        from hooks import post_gen_project

        source = open(post_gen_project.__file__, encoding="utf-8").read()
        assert '{{ cookiecutter.cloud_provider }}' in source
        assert '{{ cookiecutter.cloud_provider}}' not in source


class TestBug4CaseInsensitiveComparison:
    """Test cases for Bug 4: Case insensitive comparison inconsistency"""

    def test_cloud_provider_comparison_is_case_insensitive(self):
        """Verify cloud_provider comparison uses .lower() for case insensitivity"""
        from hooks import post_gen_project

        source = open(post_gen_project.__file__, encoding="utf-8").read()
        assert 'cloud_provider }}".lower()' in source


class TestBug5DeadCode:
    """Test cases for Bug 5: Dead code - unreachable conditional branch"""

    def test_remove_heroku_files_no_requirements_txt_check(self):
        """Verify remove_heroku_files doesn't check for requirements.txt"""
        from hooks import post_gen_project

        source = open(post_gen_project.__file__, encoding="utf-8").read()
        func_start = source.find("def remove_heroku_files()")
        func_end = source.find("\ndef ", func_start + 1)
        func_body = source[func_start:func_end]
        assert "requirements.txt" not in func_body


class TestBug6BroadExceptionCatch:
    """Test cases for Bug 6: Overly broad exception catch"""

    def test_setup_dependencies_catches_oserror_not_exception(self):
        """Verify setup_dependencies catches OSError instead of bare Exception"""
        from hooks import post_gen_project

        source = open(post_gen_project.__file__, encoding="utf-8").read()
        assert "except OSError as e:" in source
        assert "except Exception as e:  # noqa: BLE001" not in source
