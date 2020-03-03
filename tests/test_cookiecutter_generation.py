import os
import re

import pytest
from cookiecutter.exceptions import FailedHookException
import sh
import yaml
from binaryornot.check import is_binary

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)


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


SUPPORTED_COMBINATIONS = [
    {"open_source_license": "MIT"},
    {"open_source_license": "BSD"},
    {"open_source_license": "GPLv3"},
    {"open_source_license": "Apache Software License 2.0"},
    {"open_source_license": "Not open source"},
    {"windows": "y"},
    {"windows": "n"},
    {"use_pycharm": "y"},
    {"use_pycharm": "n"},
    {"use_docker": "y"},
    {"use_docker": "n"},
    {"postgresql_version": "11.3"},
    {"postgresql_version": "10.8"},
    {"postgresql_version": "9.6"},
    {"postgresql_version": "9.5"},
    {"postgresql_version": "9.4"},
    {"cloud_provider": "AWS", "use_whitenoise": "y"},
    {"cloud_provider": "AWS", "use_whitenoise": "n"},
    {"cloud_provider": "GCP", "use_whitenoise": "y"},
    {"cloud_provider": "GCP", "use_whitenoise": "n"},
    {"cloud_provider": "None", "use_whitenoise": "y"},
    # Note: cloud_provider=None AND use_whitenoise=n is not supported
    {"use_drf": "y"},
    {"use_drf": "n"},
    {"js_task_runner": "None"},
    {"js_task_runner": "Gulp"},
    {"custom_bootstrap_compilation": "y"},
    {"custom_bootstrap_compilation": "n"},
    {"use_compressor": "y"},
    {"use_compressor": "n"},
    {"use_celery": "y"},
    {"use_celery": "n"},
    {"use_mailhog": "y"},
    {"use_mailhog": "n"},
    {"use_sentry": "y"},
    {"use_sentry": "n"},
    {"use_whitenoise": "y"},
    {"use_whitenoise": "n"},
    {"use_heroku": "y"},
    {"use_heroku": "n"},
    {"ci_tool": "None"},
    {"ci_tool": "Travis"},
    {"ci_tool": "Gitlab"},
    {"keep_local_envs_in_vcs": "y"},
    {"keep_local_envs_in_vcs": "n"},
    {"debug": "y"},
    {"debug": "n"},
]

UNSUPPORTED_COMBINATIONS = [{"cloud_provider": "None", "use_whitenoise": "n"}]


def _fixture_id(ctx):
    """Helper to get a user friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in ctx.items())


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path, "r"):
            match = RE_OBJ.search(line)
            msg = "cookiecutter variable not replaced in {}"
            assert match is None, msg.format(path)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation(cookies, context, context_override):
    """Test that project is generated and fully rendered."""
    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context["project_slug"]
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flake8_passes(cookies, context_override):
    """Generated project should pass flake8."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.flake8(str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_black_passes(cookies, context_override):
    """Generated project should pass black."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.black("--check", "--diff", "--exclude", "migrations", f"{result.project}/")
    except sh.ErrorReturnCode as e:
        pytest.fail(e)


def test_travis_invokes_pytest(cookies, context):
    context.update({"ci_tool": "Travis"})
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


def test_gitlab_invokes_flake8_and_pytest(cookies, context):
    context.update({"ci_tool": "Gitlab"})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context["project_slug"]
    assert result.project.isdir()

    with open(f"{result.project}/.gitlab-ci.yml", "r") as gitlab_yml:
        try:
            gitlab_config = yaml.load(gitlab_yml)
            assert gitlab_config["flake8"]["script"] == ["flake8"]
            assert gitlab_config["pytest"]["script"] == ["pytest"]
        except yaml.YAMLError as e:
            pytest.fail(e)


@pytest.mark.parametrize("slug", ["project slug", "Project_Slug"])
def test_invalid_slug(cookies, context, slug):
    """Invalid slug should failed pre-generation hook."""
    context.update({"project_slug": slug})

    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)


@pytest.mark.parametrize("invalid_context", UNSUPPORTED_COMBINATIONS)
def test_error_if_incompatible(cookies, context, invalid_context):
    """It should not generate project an incompatible combination is selected."""
    context.update(invalid_context)
    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)
