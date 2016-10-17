project_slug = '{{ cookiecutter.project_slug }}'

if hasattr(project_slug, 'isidentifier'):
    assert project_slug.isidentifier(), 'Project slug should be valid Python identifier!'

elasticbeanstalk = '{{ cookiecutter.use_elasticbeanstalk_experimental }}'.lower()
heroku = '{{ cookiecutter.use_heroku }}'.lower()
docker = '{{ cookiecutter.use_docker }}'.lower()

if elasticbeanstalk == 'y' and (heroku == 'y' or docker == 'y'):
    raise Exception("Cookiecutter Django's EXPERIMENTAL Elastic Beanstalk support is incompatible with Heroku and Docker setups.")
