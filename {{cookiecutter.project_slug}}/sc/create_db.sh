echo 'Creating Database {{cookiecutter.project_slug}}:'
sudo -u postgres psql --command 'CREATE DATABASE {{cookiecutter.project_slug}};'

echo

echo 'Creating DB user {{cookiecutter.project_slug}}_user with password {{cookiecutter.database_user_password}}'
sudo -u postgres psql --command 'CREATE USER {{cookiecutter.project_slug}}_user WITH PASSWORD  '\'{{cookiecutter.database_user_password}}\';

echo

echo 'Altering role to utf8'
sudo -u postgres psql --command 'ALTER ROLE {{cookiecutter.project_slug}}_user SET client_encoding TO '\'utf8\';

echo

echo 'setting default_transaction_isolation TO read committed' 
sudo -u postgres psql --command 'ALTER ROLE {{cookiecutter.project_slug}}_user SET default_transaction_isolation TO '\'read\ committed\';

echo

echo 'setting timezone to {{cookiecutter.timezone}}'
sudo -u postgres psql --command 'ALTER ROLE {{cookiecutter.project_slug}}_user SET timezone TO '\'{{cookiecutter.timezone}}\';

echo

echo  'Granting all privileges on Database {{cookiecutter.project_slug}} to  {{cookiecutter.project_slug}}_user;'
sudo -u postgres psql --command 'GRANT ALL PRIVILEGES ON DATABASE {{cookiecutter.project_slug}} TO {{cookiecutter.project_slug}}_user;'
