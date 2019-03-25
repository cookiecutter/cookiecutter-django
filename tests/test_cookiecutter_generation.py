import os
import re

import pytest
import sh
import yaml
from binaryornot.check import is_binary

PATTERN = "{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)

BINARY_CHOICES = ["y", "n"]


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


@pytest.mark.parametrize("windows", BINARY_CHOICES)
@pytest.mark.parametrize("use_docker", BINARY_CHOICES)
@pytest.mark.parametrize("use_celery", BINARY_CHOICES)
@pytest.mark.parametrize("use_mailhog", BINARY_CHOICES)
@pytest.mark.parametrize("use_sentry", BINARY_CHOICES)
@pytest.mark.parametrize(
    # These 2 cannot be used together, but test the other combinations
    ["use_compressor", "use_whitenoise"],
    [("y", "n"), ("n", "n"), ("n", "n")],
)
def test_project_generation(
    cookies,
    context,
    windows,
    use_docker,
    use_celery,
    use_mailhog,
    use_sentry,
    use_compressor,
    use_whitenoise,
):
    result = cookies.bake(
        extra_context={
            **context,
            "windows": windows,
            "use_docker": use_docker,
            "use_compressor": use_compressor,
            "use_celery": use_celery,
            "use_mailhog": use_mailhog,
            "use_sentry": use_sentry,
            "use_whitenoise": use_whitenoise,
        }
    )
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context["project_slug"]
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.fixture(params=["use_mailhog", "use_celery", "windows"])
def feature_context(request, context):
    context.update({request.param: "y"})
    return context


def test_enabled_features(cookies, feature_context):
    result = cookies.bake(extra_context=feature_context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == feature_context["project_slug"]
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("windows", BINARY_CHOICES)
@pytest.mark.parametrize("use_docker", BINARY_CHOICES)
@pytest.mark.parametrize("use_celery", BINARY_CHOICES)
@pytest.mark.parametrize("use_mailhog", BINARY_CHOICES)
@pytest.mark.parametrize("use_sentry", BINARY_CHOICES)
@pytest.mark.parametrize(
    # These 2 cannot be used together, but test the other combinations
    ["use_compressor", "use_whitenoise"],
    [("y", "n"), ("n", "n"), ("n", "n")],
)
def test_linting_passes(
    cookies,
    windows,
    use_docker,
    use_celery,
    use_mailhog,
    use_sentry,
    use_compressor,
    use_whitenoise,
):
    """generated project should pass flake8"""
    result = cookies.bake(
        extra_context={
            "windows": windows,
            "use_docker": use_docker,
            "use_compressor": use_compressor,
            "use_celery": use_celery,
            "use_mailhog": use_mailhog,
            "use_sentry": use_sentry,
            "use_whitenoise": use_whitenoise,
        }
    )

    try:
        sh.flake8(str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e)

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
