git init
git add .
git commit -m "first {{cookiecutter.project_slug}} commit"
git remote add origin git@bitbucket.org:myvault/{{cookiecutter.project_slug}}.git
git push -u origin master
