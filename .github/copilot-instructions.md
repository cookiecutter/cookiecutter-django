# GitHub Copilot Instructions for cookiecutter-django

## Project Context
- This is a **Cookiecutter template**, not a standalone Django application.
- The core logic resides within the `{{cookiecutter.project_slug}}` directory.
- Files inside the template directory use **Jinja2 syntax** mixed with Python, HTML, and YAML.

## Rules for Code Generation
1. **Preserve Jinja2 Placeholders**: Do not replace or remove double curly braces like `{{cookiecutter.variable}}`. They are mandatory for template generation.
2. **Framework Context**: While the generated project is Django-based, remember that configuration files (like `settings.py`) must remain compatible with the template's conditional logic (e.g., `{% if cookiecutter.use_docker %}`).
3. **Hooks**: Pre-generation and post-generation scripts are located in `hooks/`. These are pure Python scripts that run during the scaffolding process.

## Style Guidelines
- Follow PEP 8 for Python code.
- Use double quotes for strings unless the string contains double quotes.
- Maintain the existing structure for Docker and CI/CD configurations.