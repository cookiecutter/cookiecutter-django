import cookiecutter

project_slug = '{{ cookiecutter.project_slug }}'

if hasattr(project_slug, 'isidentifier'):
    assert project_slug.isidentifier(), 'Project slug should be valid Python identifier!'

assert cookiecutter.__version__ > '1.3.0', 'Please upgrade your Cookiecutter installation'
