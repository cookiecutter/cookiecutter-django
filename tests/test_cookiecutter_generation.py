import glob
import os
import re
import sys
from collections.abc import Iterable
from pathlib import Path

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

# Run auto-fixable styles checks - skipped on CI by default. These can be fixed
# automatically by running pre-commit after generation however they are tedious
# to fix in the template, so we don't insist too much in fixing them.
AUTOFIXABLE_STYLES = os.getenv("AUTOFIXABLE_STYLES") == "1"
auto_fixable = pytest.mark.skipif(not AUTOFIXABLE_STYLES, reason="auto-fixable")


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
    {"username_type": "username"},
    {"username_type": "email"},
    {"open_source_license": "MIT"},
    {"open_source_license": "BSD"},
    {"open_source_license": "GPLv3"},
    {"open_source_license": "Apache Software License 2.0"},
    {"open_source_license": "Not open source"},
    {"windows": "y"},
    {"windows": "n"},
    {"editor": "None"},
    {"editor": "PyCharm"},
    {"editor": "VS Code"},
    {"use_docker": "y"},
    {"use_docker": "n"},
    {"postgresql_version": "16"},
    {"postgresql_version": "15"},
    {"postgresql_version": "14"},
    {"postgresql_version": "13"},
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
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Brevo"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "SparkPost"},
    {"cloud_provider": "None", "use_whitenoise": "y", "mail_service": "Other SMTP"},
    # Note: cloud_provider=None AND use_whitenoise=n is not supported
    {"cloud_provider": "AWS", "mail_service": "Mailgun"},
    {"cloud_provider": "AWS", "mail_service": "Amazon SES"},
    {"cloud_provider": "AWS", "mail_service": "Mailjet"},
    {"cloud_provider": "AWS", "mail_service": "Mandrill"},
    {"cloud_provider": "AWS", "mail_service": "Postmark"},
    {"cloud_provider": "AWS", "mail_service": "Sendgrid"},
    {"cloud_provider": "AWS", "mail_service": "Brevo"},
    {"cloud_provider": "AWS", "mail_service": "SparkPost"},
    {"cloud_provider": "AWS", "mail_service": "Other SMTP"},
    {"cloud_provider": "GCP", "mail_service": "Mailgun"},
    {"cloud_provider": "GCP", "mail_service": "Mailjet"},
    {"cloud_provider": "GCP", "mail_service": "Mandrill"},
    {"cloud_provider": "GCP", "mail_service": "Postmark"},
    {"cloud_provider": "GCP", "mail_service": "Sendgrid"},
    {"cloud_provider": "GCP", "mail_service": "Brevo"},
    {"cloud_provider": "GCP", "mail_service": "SparkPost"},
    {"cloud_provider": "GCP", "mail_service": "Other SMTP"},
    {"cloud_provider": "Azure", "mail_service": "Mailgun"},
    {"cloud_provider": "Azure", "mail_service": "Mailjet"},
    {"cloud_provider": "Azure", "mail_service": "Mandrill"},
    {"cloud_provider": "Azure", "mail_service": "Postmark"},
    {"cloud_provider": "Azure", "mail_service": "Sendgrid"},
    {"cloud_provider": "Azure", "mail_service": "Brevo"},
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
    {"use_mailpit": "y"},
    {"use_mailpit": "n"},
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
    {"ci_tool": "Drone"},
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


def build_files_list(base_path: Path):
    """Build a list containing absolute paths to the generated files."""
    return [dirpath / file_path for dirpath, subdirs, files in base_path.walk() for file_path in files]


def check_paths(paths: Iterable[Path]):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(str(path)):
            continue

        for line in path.open():
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

    paths = build_files_list(result.project_path)
    assert paths
    check_paths(paths)


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_ruff_check_passes(cookies, context_override):
    """Generated project should pass ruff check."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.ruff("check", ".", _cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_ruff_format_passes(cookies, context_override):
    """Check whether generated project passes ruff format."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.ruff(
            "format",
            ".",
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_isort_passes(cookies, context_override):
    """Check whether generated project passes isort style."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.isort(_cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_django_upgrade_passes(cookies, context_override):
    """Check whether generated project passes django-upgrade."""
    result = cookies.bake(extra_context=context_override)

    python_files = [
        file_path.removeprefix(f"{result.project_path}/")
        for file_path in glob.glob(str(result.project_path / "**" / "*.py"), recursive=True)
    ]
    try:
        sh.django_upgrade(
            "--target-version",
            "5.0",
            *python_files,
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_djlint_lint_passes(cookies, context_override):
    """Check whether generated project passes djLint --lint."""
    result = cookies.bake(extra_context=context_override)

    autofixable_rules = "H014,T001"
    # TODO: remove T002 when fixed https://github.com/Riverside-Healthcare/djLint/issues/687
    ignored_rules = "H006,H030,H031,T002"
    try:
        sh.djlint(
            "--lint",
            "--ignore",
            f"{autofixable_rules},{ignored_rules}",
            ".",
            _cwd=str(result.project_path),
        )
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@auto_fixable
@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_djlint_check_passes(cookies, context_override):
    """Check whether generated project passes djLint --check."""
    result = cookies.bake(extra_context=context_override)

    try:
        sh.djlint("--check", ".", _cwd=str(result.project_path))
    except sh.ErrorReturnCode as e:
        pytest.fail(e.stdout.decode())


@pytest.mark.parametrize(
    ("use_docker", "expected_test_script"),
    [
        ("n", "pytest"),
        ("y", "docker compose -f docker-compose.local.yml run django pytest"),
    ],
)
def test_travis_invokes_pytest(cookies, context, use_docker, expected_test_script):
    context.update({"ci_tool": "Travis", "use_docker": use_docker})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    with (result.project_path / ".travis.yml").open() as travis_yml:
        try:
            yml = yaml.safe_load(travis_yml)["jobs"]["include"]
            assert yml[0]["script"] == ["ruff check ."]
            assert yml[1]["script"] == [expected_test_script]
        except yaml.YAMLError as e:
            pytest.fail(str(e))


@pytest.mark.parametrize(
    ("use_docker", "expected_test_script"),
    [
        ("n", "pytest"),
        ("y", "docker compose -f docker-compose.local.yml run django pytest"),
    ],
)
def test_gitlab_invokes_precommit_and_pytest(cookies, context, use_docker, expected_test_script):
    context.update({"ci_tool": "Gitlab", "use_docker": use_docker})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    with (result.project_path / ".gitlab-ci.yml").open() as gitlab_yml:
        try:
            gitlab_config = yaml.safe_load(gitlab_yml)
            assert gitlab_config["precommit"]["script"] == [
                "pre-commit run --show-diff-on-failure --color=always --all-files",
            ]
            assert gitlab_config["pytest"]["script"] == [expected_test_script]
        except yaml.YAMLError as e:
            pytest.fail(e)


@pytest.mark.parametrize(
    ("use_docker", "expected_test_script"),
    [
        ("n", "pytest"),
        ("y", "docker compose -f docker-compose.local.yml run django pytest"),
    ],
)
def test_github_invokes_linter_and_pytest(cookies, context, use_docker, expected_test_script):
    context.update({"ci_tool": "Github", "use_docker": use_docker})
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    with (result.project_path / ".github" / "workflows" / "ci.yml").open() as github_yml:
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
    ("editor", "pycharm_docs_exist"),
    [
        ("None", False),
        ("PyCharm", True),
        ("VS Code", False),
    ],
)
def test_pycharm_docs_removed(cookies, context, editor, pycharm_docs_exist):
    context.update({"editor": editor})
    result = cookies.bake(extra_context=context)

    index_rst = result.project_path / "docs" / "index.rst"
    has_pycharm_docs = "pycharm/configuration" in index_rst.read_text()
    assert has_pycharm_docs is pycharm_docs_exist


def test_trim_domain_email(cookies, context):
    """Check that leading and trailing spaces are trimmed in domain and email."""
    context.update(
        {
            "use_docker": "y",
            "domain_name": "   example.com   ",
            "email": "  me@example.com  ",
        },
    )
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0

    prod_django_env = result.project_path / ".envs" / ".production" / ".django"
    assert "DJANGO_ALLOWED_HOSTS=.example.com" in prod_django_env.read_text()

    base_settings = result.project_path / "config" / "settings" / "base.py"
    assert '"me@example.com"' in base_settings.read_text()
