import os
import re

import pytest
import sh
import yaml
from binaryornot.check import is_binary

PATTERN = "{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)

BINARY_CHOICES = ["y", "n"]
JS_TASK_RUNNER_CHOICES = ["None", "Gulp"]


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


def test_default_configuration(cookies, context):
    result = cookies.bake(extra_context=context)
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
@pytest.mark.parametrize("use_pycharm", BINARY_CHOICES)
@pytest.mark.parametrize("use_docker", BINARY_CHOICES)
@pytest.mark.parametrize("js_task_runner", JS_TASK_RUNNER_CHOICES)
@pytest.mark.parametrize("custom_bootstrap_compilation", BINARY_CHOICES)
@pytest.mark.parametrize("use_celery", BINARY_CHOICES)
@pytest.mark.parametrize("use_mailhog", BINARY_CHOICES)
@pytest.mark.parametrize("use_sentry", BINARY_CHOICES)
@pytest.mark.parametrize(
    # These 2 cannot be used together, but test the other combinations
    ["use_compressor", "use_whitenoise"],
    [("y", "n"), ("n", "n"), ("n", "n")],
)
@pytest.mark.parametrize("use_heroku", BINARY_CHOICES)
@pytest.mark.parametrize("use_travisci", BINARY_CHOICES)
@pytest.mark.parametrize("keep_local_envs_in_vcs", BINARY_CHOICES)
def test_flake8_compliance(
    cookies,
    windows,
    use_pycharm,
    use_docker,
    js_task_runner,
    custom_bootstrap_compilation,
    use_celery,
    use_mailhog,
    use_sentry,
    use_compressor,
    use_whitenoise,
    use_heroku,
    use_travisci,
    keep_local_envs_in_vcs,
):
    """generated project should pass flake8"""
    result = cookies.bake(
        extra_context={
            "windows": windows,
            "use_pycharm": use_pycharm,
            "use_docker": use_docker,
            "js_task_runner": js_task_runner,
            "custom_bootstrap_compilation": custom_bootstrap_compilation,
            "use_compressor": use_compressor,
            "use_celery": use_celery,
            "use_mailhog": use_mailhog,
            "use_sentry": use_sentry,
            "use_whitenoise": use_whitenoise,
            "use_heroku": use_heroku,
            "use_travisci": use_travisci,
            "keep_local_envs_in_vcs": keep_local_envs_in_vcs,
        }
    )

    try:
        sh.flake8(str(result.project))
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
