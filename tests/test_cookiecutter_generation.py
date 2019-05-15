import os
import re

import pytest
from pytest_cases import pytest_fixture_plus
import sh
import yaml
from binaryornot.check import is_binary

PATTERN = "{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)

YN_CHOICES = ["y", "n"]
CLOUD_CHOICES = ["AWS", "GCE"]


@pytest.fixture
def context():
    return {
        "project_name": "My Test Project",
        "project_slug": "my_test_project",
        "author_name": "Test Author",
        "email": "test@example.com",
        "description": "A short description of the project.",
        "domain_name": "example.com",
        "version": "0.1.0",
        "timezone": "UTC",
    }


@pytest_fixture_plus
@pytest.mark.parametrize("windows", YN_CHOICES, ids=lambda yn: f"win:{yn}")
@pytest.mark.parametrize("use_docker", YN_CHOICES, ids=lambda yn: f"docker:{yn}")
@pytest.mark.parametrize("use_celery", YN_CHOICES, ids=lambda yn: f"celery:{yn}")
@pytest.mark.parametrize("use_mailhog", YN_CHOICES, ids=lambda yn: f"mailhog:{yn}")
@pytest.mark.parametrize("use_sentry", YN_CHOICES, ids=lambda yn: f"sentry:{yn}")
@pytest.mark.parametrize("use_compressor", YN_CHOICES, ids=lambda yn: f"cmpr:{yn}")
@pytest.mark.parametrize("use_whitenoise", YN_CHOICES, ids=lambda yn: f"wnoise:{yn}")
@pytest.mark.parametrize("cloud_provider", CLOUD_CHOICES, ids=lambda yn: f"cloud:{yn}")
def context_combination(
    windows,
    use_docker,
    use_celery,
    use_mailhog,
    use_sentry,
    use_compressor,
    use_whitenoise,
    cloud_provider,
):
    """Fixture that parametrize the function where it's used."""
    return {
        "windows": windows,
        "use_docker": use_docker,
        "use_compressor": use_compressor,
        "use_celery": use_celery,
        "use_mailhog": use_mailhog,
        "use_sentry": use_sentry,
        "use_whitenoise": use_whitenoise,
        "cloud_provider": cloud_provider,
    }


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions,
    used by other tests cases
    """
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path, "r"):
            match = RE_OBJ.search(line)
            msg = "cookiecutter variable not replaced in {}"
            assert match is None, msg.format(path)


def test_project_generation(cookies, context, context_combination):
    """
    Test that project is generated and fully rendered.

    This is parametrized for each combination from ``context_combination`` fixture
    """
    result = cookies.bake(extra_context={**context, **context_combination})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context["project_slug"]
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.flake8
def test_flake8_passes(cookies, context_combination):
    """
    Generated project should pass flake8.

    This is parametrized for each combination from ``context_combination`` fixture
    """
    result = cookies.bake(extra_context=context_combination)

    try:
        sh.flake8(str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e)


@pytest.mark.black
def test_black_passes(cookies, context_combination):
    """
    Generated project should pass black.

    This is parametrized for each combination from ``context_combination`` fixture
    """
    result = cookies.bake(extra_context=context_combination)

    try:
        sh.black("--check", "--diff", "--exclude", "migrations", f"{result.project}/")
    except sh.ErrorReturnCode as e:
        pytest.fail(e)


def test_travis_invokes_pytest(cookies, context):
    context.update({"use_travisci": "y"})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context["project_slug"]
    assert result.project.isdir()

    with open(f"{result.project}/.travis.yml", "r") as travis_yml:
        try:
            assert yaml.load(travis_yml)["script"] == ["pytest"]
        except yaml.YAMLError as e:
            pytest.fail(e)
