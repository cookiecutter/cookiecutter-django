project_slug = '{{ cookiecutter.project_slug }}'

if hasattr(project_slug, 'isidentifier'):
    assert project_slug.isidentifier(), 'Project slug should be valid Python identifier!'
