import os
import re

import pytest
from cookiecutter.exceptions import FailedHookException
from pytest_cases import fixture_plus
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


@fixture_plus
@pytest.mark.parametrize("windows", ["y", "n"], ids=lambda yn: f"win:{yn}")
@pytest.mark.parametrize("use_docker", ["y", "n"], ids=lambda yn: f"docker:{yn}")
@pytest.mark.parametrize("use_celery", ["y", "n"], ids=lambda yn: f"celery:{yn}")
@pytest.mark.parametrize("use_mailhog", ["y", "n"], ids=lambda yn: f"mailhog:{yn}")
@pytest.mark.parametrize("use_sentry", ["y", "n"], ids=lambda yn: f"sentry:{yn}")
@pytest.mark.parametrize("use_compressor", ["y", "n"], ids=lambda yn: f"cmpr:{yn}")
@pytest.mark.parametrize("use_drf", ["y", "n"], ids=lambda yn: f"drf:{yn}")
@pytest.mark.parametrize(
    "use_whitenoise,cloud_provider",
    [
        ("y", "AWS"),
        ("y", "GCP"),
        ("y", "None"),
        ("n", "AWS"),
        ("n", "GCP"),
        # no whitenoise + no cloud provider is not supported
    ],
    ids=lambda id: f"wnoise:{id[0]}-cloud:{id[1]}",
)
@pytest.mark.parametrize(
    "mail_service",
    [
        "Amazon SES",
        "Mailgun",
        "MailJet",
        "Mandrill",
        "Postmark",
        "Sendgrid",
        "SendinBlue",
        "SparkPost",
        "Plain/Vanilla Django-Anymail"
        # GCP or None (i.e. no cloud provider) + Amazon SES is not supported
    ],
    ids=lambda id: f"mail:{id[0]}",
)
def context_combination(
    windows,
    use_docker,
    use_celery,
    use_mailhog,
    use_sentry,
    use_compressor,
    use_whitenoise,
    use_drf,
    cloud_provider,
    mail_service,
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
        "use_drf": use_drf,
        "cloud_provider": cloud_provider,
        "mail_service": mail_service,
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


def test_no_whitenoise_and_no_cloud_provider(cookies, context):
    """It should not generate project if neither whitenoise or cloud provider are set"""
    context.update({"use_whitenoise": "n", "cloud_provider": "None"})
    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)


def test_gcp_with_aws_ses_mail_service(cookies, context):
    """It should not generate project if SES is set with GCP cloud provider"""
    context.update({"cloud_provider": "GCP", "mail_service": "Amazon SES"})
    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)


def test_no_cloud_provider_with_aws_ses_mail_service(cookies, context):
    """It should not generate project if SES is set with no cloud provider"""
    context.update({"cloud_provider": "None", "mail_service": "Amazon SES"})
    result = cookies.bake(extra_context=context)

    assert result.exit_code != 0
    assert isinstance(result.exception, FailedHookException)
