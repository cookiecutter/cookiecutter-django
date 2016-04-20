repo_name = '{{ cookiecutter.project_slug }}'

if hasattr(repo_name, 'isidentifier'):
    assert repo_name.isidentifier(), 'Repo name should be valid Python identifier!'
