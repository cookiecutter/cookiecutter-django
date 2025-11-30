# Cookiecutter Django - AI Coding Agent Instructions

## Project Architecture

This is a **Cookiecutter template** for Django projects, not a standard Django application. The actual project structure exists in `{{cookiecutter.project_slug}}/` which contains Jinja2 template syntax (`{{ }}`, `{% %}`) that gets rendered when users run `cookiecutter` to generate a new Django project.

### Key Directories
- `{{cookiecutter.project_slug}}/` - Template for generated Django projects with Jinja2 variables
- `hooks/` - Python scripts that run before/after project generation (`pre_gen_project.py`, `post_gen_project.py`)
- `tests/` - Template generation tests using pytest-cookies
- `docs/` - Project documentation (separate from generated project docs)
- `scripts/` - Maintenance utilities (version bumps, changelog updates)

### Template Rendering Flow
1. User runs `cookiecutter` with configuration choices in `cookiecutter.json`
2. `hooks/pre_gen_project.py` validates choices (e.g., project_slug format, cloud provider compatibility)
3. Jinja2 renders all `{{cookiecutter.*}}` variables and `{% if %}` conditionals
4. `hooks/post_gen_project.py` removes unused files based on choices (Docker, Celery, frontend pipeline, etc.)

## Critical Development Workflows

### Running Template Tests
```bash
# Test template generation (fast)
uv run tox run -e py

# Test specific scenario
uv run tox run -e py -- -k test_default_configuration

# Full integration tests (slow)
tests/test_bare.sh use_celery=y  # Without Docker
tests/test_docker.sh use_docker=y  # With Docker
```

### Testing Generated Projects
The template produces different outputs based on `cookiecutter.json` choices. Test scripts generate projects, install dependencies, and run their test suites:
- `test_bare.sh` - Bare metal setup (no Docker)
- `test_docker.sh` - Docker-based setup with compose files

### Docker Commands for Generated Projects
Generated projects use Docker Compose with different configs:
```bash
# Local development
docker compose -f docker-compose.local.yml up
docker compose -f docker-compose.local.yml run --rm django pytest
docker compose -f docker-compose.local.yml run django uv lock  # Generate lockfile

# Production setup
docker compose -f docker-compose.production.yml build
docker compose -f docker-compose.production.yml up -d
```

Generated projects may include a `justfile` with shortcuts:
```bash
just up              # Start containers
just manage migrate  # Run Django management commands
just logs django     # View service logs
```

## Project-Specific Conventions

### Jinja2 Template Syntax
All files in `{{cookiecutter.project_slug}}/` contain template variables:
- `{{ cookiecutter.project_slug }}` - User's project name
- `{% if cookiecutter.use_docker == 'y' %}...{% endif %}` - Conditional sections
- `{%- if ... -%}` - Whitespace control (important for Python indentation)

**Never edit template files without preserving Jinja2 syntax.** Example from `base.py`:
```python
TIME_ZONE = "{{ cookiecutter.timezone }}"
{% if cookiecutter.use_docker == "y" -%}
DATABASES = {"default": env.db("DATABASE_URL")}
{%- else %}
DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///{{cookiecutter.project_slug}}")}
{%- endif %}
```

### Hook System
`hooks/post_gen_project.py` contains cleanup logic that removes files based on user choices:
- `remove_docker_files()` if `use_docker == 'n'`
- `remove_celery_files()` if `use_celery == 'n'`
- `handle_js_runner()` configures Gulp/Webpack or removes frontend tooling

When adding new optional features, update both the template files AND the corresponding removal function in hooks.

### Configuration Matrix Testing
`tests/test_cookiecutter_generation.py` defines `SUPPORTED_COMBINATIONS` - a matrix of valid configuration options. Each combination is tested to ensure:
- Valid project generation (no Jinja2 errors)
- No unrendered template variables remain (regex check)
- Basic linting passes (ruff)

Add new combinations when introducing features with interdependencies (e.g., `cloud_provider` + `mail_service`).

## Integration Points

### Dependency Management
Generated projects use **uv** for Python dependencies with lockfiles:
- Template root: `pyproject.toml` defines template dev dependencies (cookiecutter, pytest-cookies, ruff)
- Generated projects: `{{cookiecutter.project_slug}}/pyproject.toml` defines Django app dependencies
- Docker builds run `uv sync` to install from lockfiles

### CI/CD Configuration
Templates include conditional CI configs:
- `{% if cookiecutter.ci_tool == 'Github' %}` generates `.github/workflows/ci.yml`
- `{% if cookiecutter.ci_tool == 'Gitlab' %}` generates `.gitlab-ci.yml`

CI tests both linting and project tests with environment-specific commands (Docker vs bare metal).

### Settings Architecture
Generated projects use django-environ with three settings modules:
- `config/settings/base.py` - Shared settings with Jinja2 variables
- `config/settings/local.py` - Development settings
- `config/settings/production.py` - Production with cloud provider integrations

Environment variables read from `.envs/.local/` or `.envs/.production/` directories in Docker setups.

## Common Patterns

### Adding Optional Features
1. Add choice to `cookiecutter.json` with default
2. Add conditional blocks in template files: `{% if cookiecutter.new_feature == 'y' %}`
3. Create removal function in `hooks/post_gen_project.py`
4. Update test matrix in `tests/test_cookiecutter_generation.py`
5. Document in `docs/1-getting-started/project-generation-options.rst`

### Version Bumps
Use maintenance scripts instead of manual edits:
- `scripts/node_version.py` - Update Node.js versions across Dockerfiles, package.json, CI
- `scripts/ruff_version.py` - Update Ruff versions in pyproject.toml files
- `scripts/update_changelog.py` - Generate changelog entries

### Pre-commit Configuration
Both template and generated projects use pre-commit with ruff for linting. Auto-fixable style issues are skipped in CI via `AUTOFIXABLE_STYLES` env var since they're tedious to fix in Jinja2 templates.

