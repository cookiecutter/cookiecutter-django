rm -rf db.sqli*
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
. ./makemigrations.sh
. ./migrate.sh
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'Amman123')" | python manage.py shell
