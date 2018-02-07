project_slug = '{{ cookiecutter.project_slug }}'

if hasattr(project_slug, 'isidentifier'):
    assert project_slug.isidentifier(), 'Project slug should be valid Python identifier!'

heroku = '{{ cookiecutter.use_heroku }}'.lower()
docker = '{{ cookiecutter.use_docker }}'.lower()

if docker == 'n':
	import sys

	python_major_version = sys.version_info[0]

	if python_major_version == 2:
		sys.stdout.write("WARNING: Cookiecutter Django does not support Python 2! Stability is guaranteed with Python 3.6+ only. Are you sure you want to proceed? (y/n)")

		yes_options = set(['y'])
		no_options = set(['n', ''])
		choice = raw_input().lower()
		if choice in no_options:
			sys.exit(1)
		elif choice in yes_options:
			pass
		else:
			sys.stdout.write("Please respond with %s or %s"
				% (', '.join([o for o in yes_options if not o == ''])
					, ', '.join([o for o in no_options if not o == ''])))
