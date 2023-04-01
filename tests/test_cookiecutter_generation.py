import os
import re
import sys

import pytest

try:
    import sh
except (ImportError, ModuleNotFoundError):
    sh = None  # sh doesn't support Windows
import yaml
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)

if sys.platform.startswith("win"):
    pytest.skip("sh doesn't support windows", allow_module_level=True)
elif sys.platform.startswith("darwin") and os.getenv("CI"):
    pytest.skip("skipping slow macOS tests on CI", allow_module_level=True)


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
    {"postgresql_version": "14"},
    {"postgresql_version": "13"},
    {"postgresql_version": "12"},
    {"postgresql_version": "11"},
    {"postgresql_version": "10"},
    {"cloud_provider": "AWS", "use_whitenoise": "y"},
    {"cloud_provider": "AWS", "use_whitenoise": "n"},
    {"cloud_provider": "GCP", "use_whitenoise": "y"},
    {"cloud_provider": "GCP", "use_whitenoise": "n"},
    {"cloud_provider": "Azure", "use_whitenoise": "y"},
    {"cloud_provider": "Azure", "use_whitenoise": "n"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Mailgun"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Mailjet"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Mandrill"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Postmark"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Sendgrid"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "SendinBlue"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "SparkPost"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Other SMTP"},
    # Note: cloud_provider=None AND use_whitenoise=n is not supported
    {"cloud_provider": "AWS", "mail_service": "Mailgun"},
    {"cloud_provider": "AWS", "mail_service": "Amazon SES"},
    {"cloud_provider": "AWS", "mail_service": "Mailjet"},
    {"cloud_provider": "AWS", "mail_service": "Mandrill"},
    {"cloud_provider": "AWS", "mail_service": "Postmark"},
    {"cloud_provider": "AWS", "mail_service": "Sendgrid"},
    {"cloud_provider": "AWS", "mail_service": "SendinBlue"},
    {"cloud_provider": "AWS", "mail_service": "SparkPost"},
    {"cloud_provider": "AWS", "mail_service": "Other SMTP"},
    {"cloud_provider": "GCP", "mail_service": "Mailgun"},
    {"cloud_provider": "GCP", "mail_service": "Mailjet"},
    {"cloud_provider": "GCP", "mail_service": "Mandrill"},
    {"cloud_provider": "GCP", "mail_service": "Postmark"},
    {"cloud_provider": "GCP", "mail_service": "Sendgrid"},
    {"cloud_provider": "GCP", "mail_service": "SendinBlue"},
    {"cloud_provider": "GCP", "mail_service": "SparkPost"},
    {"cloud_provider": "GCP", "mail_service": "Other SMTP"},
    {"cloud_provider": "Azure", "mail_service": "Mailgun"},
    {"cloud_provider": "Azure", "mail_service": "Mailjet"},
    {"cloud_provider": "Azure", "mail_service": "Mandrill"},
    {"cloud_provider": "Azure", "mail_service": "Postmark"},
    {"cloud_provider": "Azure", "mail_service": "Sendgrid"},
    {"cloud_provider": "Azure", "mail_service": "SendinBlue"},
    {"cloud_provider": "Azure", "mail_service": "SparkPost"},
    {"cloud_provider": "Azure", "mail_service": "Other SMTP"},
    # Note: cloud_providers GCP, Azure, and None
    # with mail_service Amazon SES is not supported
    {"use_async": "y"},
    {"use_async": "n"},
    {"use_drf": "y"},
    {"use_drf": "n"},
    {"frontend_pipeline": "None"},
    {"frontend_pipeline": "Django Compressor"},
    {"frontend_pipeline": "Gulp"},
    {"frontend_pipeline": "Webpack"},
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
    {"ci_tool": "Github"},
    {"keep_local_envs_in_vcs": "y"},
    {"keep_local_envs_in_vcs": "n"},
    {"debug": "y"},
    {"debug": "n"},
]

UNSUPPORTED_COMBINATIONS = [
    {"cloud_provider": "None", "use_whitenoise": "n"},
    {"cloud_provider": "GCP", "mail_service": "Amazon SES"},
    {"cloud_provider": "Azure", "mail_service": "Amazon SES"},
    {"cloud_provider": "None", "mail_service": "Amazon SES"},
]


def _fixture_id(ctx):
    """Helper to get a user-friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in ctx.items())


def build_files_list(base_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(base_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path):
            match = RE_OBJ.search(line)
            assert match is None, f"cookiecutter variable not replaced in {path}"


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation(cookies, context, context_override):
    """Test that project is generated and fully rendered."""

    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    paths = build_files_list(str(result.project_path))
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_flake8_passes(cookies, context_override):
    """Generated project should pass flake8."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.flake8(_cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_black_passes(cookies, context_override):
    """Generated project should pass black."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.black(
            "--check",
            "--diff",
            "--exclude",
            "migrations",
            ".",
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize(
    ["use_docker", "expected_test_script"],
    [
        ("n", "pytest"),
        ("y", "docker-compose -f local.yml run django pytest"),
    ],
)
def test_travis_invokes_pytest(cookies, context, use_docker, expected_test_script):
    context.update({"ci_tool": "Travis", "use_docker": use_docker})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    with open(f"{result.project_path}/.travis.yml") as travis_yml:
        try:
            yml = yaml.safe_load(travis_yml)["jobs"]["include"]
            assert yml[0]["script"] == ["flake8"]
            assert yml[1]["script"] == [expected_test_script]
        except yaml.YAMLError as e:
            pytest.fail(str(e))


@pytest.mark.parametrize(
    ["use_docker", "expected_test_script"],
    [
        ("n", "pytest"),
        ("y", "docker-compose -f local.yml run django pytest"),
    ],
)
def test_gitlab_invokes_precommit_and_pytest(
    cookies, context, use_docker, expected_test_script
):
    context.update({"ci_tool": "Gitlab", "use_docker": use_docker})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    with open(f"{result.project_path}/.gitlab-ci.yml") as gitlab_yml:
        try:
            gitlab_config = yaml.safe_load(gitlab_yml)
            assert gitlab_config["precommit"]["script"] == [
                "pre-commit run --show-diff-on-failure --color=always --all-files"
            ]
            assert gitlab_config["pytest"]["script"] == [expected_test_script]
        except yaml.YAMLError as e:
            pytest.fail(e)


@pytest.mark.parametrize(
    ["use_docker", "expected_test_script"],
    [
        ("n", "pytest"),
        ("y", "docker-compose -f local.yml run django pytest"),
    ],
)
def test_github_invokes_linter_and_pytest(
    cookies, context, use_docker, expected_test_script
):
    context.update({"ci_tool": "Github", "use_docker": use_docker})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    with open(f"{result.project_path}/.github/workflows/ci.yml") as github_yml:
        try:
            github_config = yaml.safe_load(github_yml)
            linter_present = False
            for action_step in github_config["jobs"]["linter"]["steps"]:
                if action_step.get("uses", "NA").startswith("pre-commit"):
                    linter_present = True
            assert linter_present

            expected_test_script_present = False
            for action_step in github_config["jobs"]["pytest"]["steps"]:
                if action_step.get("run") == expected_test_script:
                    expected_test_script_present = True
            assert expected_test_script_present
        except yaml.YAMLError as e:
            pytest.fail(e)


@pytest.mark.parametrize("slug", ["project slug", "Project_Slug"])
def test_invalid_slug(cookies, context, slug):
    """Invalid slug should fail pre-generation hook."""
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


@pytest.mark.parametrize(
    ["use_pycharm", "pycharm_docs_exist"],
    [
        ("n", False),
        ("y", True),
    ],
)
def test_pycharm_docs_removed(cookies, context, use_pycharm, pycharm_docs_exist):
    context.update({"use_pycharm": use_pycharm})
    result = cookies.bake(extra_context=context)

    with open(f"{result.project_path}/docs/index.rst") as f:
        has_pycharm_docs = "pycharm/configuration" in f.read()
        assert has_pycharm_docs is pycharm_docs_exist


def test_trim_domain_email(cookies, context):
    """Check that leading and trailing spaces are trimmed in domain and email."""
    context.update(
        {
            "use_docker": "y",
            "domain_name": "   example.com   ",
            "email": "  me@example.com  ",
        }
    )
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    prod_django_env = result.project_path / ".envs" / ".production" / ".django"
    assert "DJANGO_ALLOWED_HOSTS=.example.com" in prod_django_env.read_text()

    base_settings = result.project_path / "config" / "settings" / "base.py"
    assert '"me@example.com"' in base_settings.read_text()
