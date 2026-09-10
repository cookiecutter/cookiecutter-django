import glob  # noqa: EXE002
import hashlib
import json
import os
import re
import sys
from collections.abc import Iterable
from pathlib import Path

import pytest
import tomllib

try:
    import sh
except (ImportError, ModuleNotFoundError):
    sh = None  # sh doesn't support Windows
import yaml
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)
# <script src="http(s)://..."> or <link href="http(s)://...">
RE_REMOTE_ASSET = re.compile(r"<(?:script|link)\b[^>]*\b(?:src|href)=[\"']https?://", re.IGNORECASE)

# Paths that must never be generated any more (Node.js / asset pipeline leftovers)
FRONTEND_TOOLCHAIN_PATHS = [
    "package.json",
    "package-lock.json",
    "gulpfile.mjs",
    "webpack",
    "compose/local/node",
    "my_test_project/static/sass",
    "my_test_project/static/js/vendors.js",
]
# Case-insensitive tokens that must not appear in any generated text file
FRONTEND_TOOLCHAIN_TOKENS = [
    "bootstrap",
    "crispy",
    "compressor",
    "compress_",
    "webpack",
    "gulp",
    "node_modules",
    "docker.io/node",
    "npm ",
    "cdnjs",
    "sass",
]

if sys.platform.startswith("win"):
    pytest.skip("sh doesn't support windows", allow_module_level=True)
elif sys.platform.startswith("darwin") and os.getenv("CI"):
    pytest.skip("skipping slow macOS tests on CI", allow_module_level=True)

# Run auto-fixable styles checks - skipped on CI by default. These can be fixed
# automatically by running pre-commit after generation. However, they are tedious
# to fix in the template, so we don't insist too much on fixing them.
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
    {"postgresql_version": "18"},
    {"postgresql_version": "17"},
    {"postgresql_version": "16"},
    {"postgresql_version": "15"},
    {"postgresql_version": "14"},
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
    {"rest_api": "None"},
    {"rest_api": "DRF"},
    {"rest_api": "Django Ninja"},
    {"use_async": "y"},
    {"use_async": "n"},
    {"use_celery": "y"},
    {"use_celery": "n"},
    {"mail_catcher": "None"},
    {"mail_catcher": "Mailpit"},
    {"mail_catcher": "Mailtrap Local"},
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
    excluded_dirs = {".venv", "__pycache__"}

    f = []
    for dirpath, subdirs, files in base_path.walk():
        subdirs[:] = [d for d in subdirs if d not in excluded_dirs]

        f.extend(dirpath / file_path for file_path in files)
    return f


def check_paths(paths: Iterable[Path]):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(str(path)):
            continue

        content = path.read_text()
        match = RE_OBJ.search(content)
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
def test_django_upgrade_passes(cookies, context_override):
    """Check whether generated project passes django-upgrade."""
    result = cookies.bake(extra_context=context_override)

    python_files = [
        file_path.removeprefix(f"{result.project_path}/")
        for file_path in glob.glob(str(result.project_path / "**" / "*.py"), recursive=True)  # noqa: PTH207
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


# (use_docker, type-check command, test command) as the generated CI configs must invoke them.
CI_SCRIPT_CASES = [
    ("n", "uv run mypy .", "uv run pytest"),
    (
        "y",
        "docker compose -f docker-compose.local.yml run --rm django mypy .",
        "docker compose -f docker-compose.local.yml run django pytest",
    ),
]


@pytest.mark.parametrize(
    ("use_docker", "expected_typecheck_script", "expected_test_script"),
    CI_SCRIPT_CASES,
)
def test_travis_invokes_mypy_and_pytest(
    cookies,
    context,
    use_docker,
    expected_typecheck_script,
    expected_test_script,
):
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
            assert yml[1]["script"] == [expected_typecheck_script, expected_test_script]
        except yaml.YAMLError as e:
            pytest.fail(str(e))


@pytest.mark.parametrize(
    ("use_docker", "expected_typecheck_script", "expected_test_script"),
    CI_SCRIPT_CASES,
)
def test_gitlab_invokes_precommit_mypy_and_pytest(
    cookies,
    context,
    use_docker,
    expected_typecheck_script,
    expected_test_script,
):
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
                "uv run pre-commit run --show-diff-on-failure --color=always --all-files",
            ]
            assert gitlab_config["pytest"]["script"] == [
                expected_typecheck_script,
                expected_test_script,
            ]
        except yaml.YAMLError as e:
            pytest.fail(e)


@pytest.mark.parametrize(
    ("use_docker", "expected_typecheck_script", "expected_test_script"),
    CI_SCRIPT_CASES,
)
def test_github_invokes_linter_mypy_and_pytest(
    cookies,
    context,
    use_docker,
    expected_typecheck_script,
    expected_test_script,
):
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

            typecheck_steps = [step.get("run") for step in github_config["jobs"]["typecheck"]["steps"]]
            assert expected_typecheck_script in typecheck_steps

            pytest_steps = [step.get("run") for step in github_config["jobs"]["pytest"]["steps"]]
            assert expected_test_script in pytest_steps
            assert expected_typecheck_script not in pytest_steps
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
    assert "<me@example.com>" in base_settings.read_text()


def test_pyproject_toml(cookies, context):
    author_name = "Project Author"
    author_email = "me@example.com"
    context.update(
        {
            "description": "DESCRIPTION",
            "domain_name": "example.com",
            "email": author_email,
            "author_name": author_name,
        },
    )
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject_toml = result.project_path / "pyproject.toml"

    data = tomllib.loads(pyproject_toml.read_text())

    assert data
    assert data["project"]["authors"][0]["email"] == author_email
    assert data["project"]["authors"][0]["name"] == author_name
    assert data["project"]["name"] == context["project_slug"]


@pytest.mark.parametrize("rest_api", ["None", "DRF", "Django Ninja"])
def test_strict_typing_setup(cookies, context, rest_api):
    """The generated project is type checked in strict mode with the right plugins and request types."""
    context.update({"rest_api": rest_api})
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pyproject = (result.project_path / "pyproject.toml").read_text()
    assert "strict = true" in pyproject
    assert "mypy_django_plugin.main" in pyproject
    assert ("mypy_drf_plugin.main" in pyproject) is (rest_api == "DRF")
    assert ("runtime-evaluated-decorators" in pyproject) is (rest_api == "Django Ninja")

    typedefs = (result.project_path / context["project_slug"] / "typedefs.py").read_text()
    assert "class AuthenticatedHttpRequest(HttpRequest):" in typedefs
    assert "class AuthenticatedHtmxRequest(" in typedefs
    assert ("class AuthenticatedApiRequest(Request):" in typedefs) is (rest_api == "DRF")


def test_pre_commit_without_heroku(cookies, context):
    context.update({"use_heroku": "n"})
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    pre_commit_config = result.project_path / ".pre-commit-config.yaml"

    data = pre_commit_config.read_text()

    assert "uv-pre-commit" not in data


def test_frontend_stack(cookies, context):
    """Generated project uses django-htmx + vendored Pico CSS and has no Node.js/asset pipeline leftovers."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    for path in FRONTEND_TOOLCHAIN_PATHS:
        assert not (result.project_path / path).exists(), f"{path} should not be generated"

    offenders = []
    for path in build_files_list(result.project_path):
        if "static/vendor/" in path.as_posix() or is_binary(str(path)):
            continue
        content = path.read_text().lower()
        offenders.extend(f"{path}: {token}" for token in FRONTEND_TOOLCHAIN_TOKENS if token in content)
    assert offenders == []

    settings = (result.project_path / "config" / "settings" / "base.py").read_text()
    assert '"django_htmx",' in settings
    assert '"django_htmx.middleware.HtmxMiddleware",' in settings
    assert "django-htmx==" in (result.project_path / "pyproject.toml").read_text()

    base_html = (result.project_path / "my_test_project" / "templates" / "base.html").read_text()
    assert "{% htmx_script %}" in base_html
    assert 'hx-headers=\'{"X-CSRFToken": "{{ csrf_token }}"}\'' in base_html
    assert "vendor/pico/pico.min.css" in base_html


def test_no_remote_assets(cookies, context):
    """No stylesheet or script is loaded from a CDN or any other remote host."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    offenders = [
        path
        for path in build_files_list(result.project_path)
        if path.suffix == ".html" and RE_REMOTE_ASSET.search(path.read_text())
    ]
    assert offenders == []


def test_vendored_pico_intact(cookies, context):
    """The vendored Pico CSS is copied byte-for-byte and matches its recorded checksum."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0

    vendor_dir = result.project_path / "my_test_project" / "static" / "vendor" / "pico"
    metadata = json.loads((vendor_dir / "pico.json").read_text())
    css = (vendor_dir / metadata["file"]).read_bytes()

    assert hashlib.sha256(css).hexdigest() == metadata["sha256"]
    assert f"v{metadata['version']}".encode() in css[:300]
    assert (vendor_dir / "LICENSE.md").read_text().startswith("MIT License")
