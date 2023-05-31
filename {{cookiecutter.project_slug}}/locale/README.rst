Translations
============

Translations strings will be placed in this folder when running::

    {% if cookiecutter.use_docker == 'y' %}docker-compose -f local.yml run --rm django {% endif %}python manage.py makemessages -all --no-location

This should generate ``django.po`` (stands for Portable Object) files under each locale `<locale name>/LC_MESSAGES/django.po`. Each translatable string in the codebase is collected with its ``msgid`` and need to be translated as ``msgstr``, for example::

    msgid "users"
    msgstr "utilisateurs"

Once all translations are done, they need to be compiled into ``.mo`` files (stands for Machine Object), which are the actual binary files used by the application::

    {% if cookiecutter.use_docker == 'y' %}docker-compose -f local.yml run --rm django {% endif %}python manage.py compilemessages

Note that the ``.po`` files are NOT used by the application directly, so if the ``.mo`` files are out of dates, the content won't appear as translated even if the ``.po`` files are up to date.

The production image runs ``compilemessages`` automatically at build time, so as long as your translated source files (PO) are up to date, you're good to go.
