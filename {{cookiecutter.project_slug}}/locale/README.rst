Translations
============

Translations strings will be placed in this folder when running::

    python manage.py makemessages -all

This should generate ``django.po`` (stands for Portable Object) files under each locale `<locale name>/LC_MESSAGES/django.po`. Each translatable string in the codebase is collected with its ``msgid`` and need to be translated as ``msgstr``, for example::

    msgid "users"
    msgstr "utilisateurs"

Once all translations are done, they need to be compiled into ``.mo`` files (stands for Machine Object), which are the actual binary files used by the application::

    python manage.py compilemessages

Note that the ``.po`` files are NOT used by the application directly, so if the ``.mo`` files are out of dates, the content won't appear as translated even if the ``.po`` files are up to date.
