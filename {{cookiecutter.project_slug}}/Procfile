release: python manage.py migrate
web: gunicorn config.wsgi:application
{% if cookiecutter.use_celery == "y" -%}
worker: celery worker --app=config.celery_app --loglevel=info
{%- endif %}
