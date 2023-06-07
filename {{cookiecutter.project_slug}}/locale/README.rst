Translations
============

Start by configuring `LANGUAGES` at settings, by uncommenting languages you are willing to support.

Translations will be placed in this folder when running:

    python manage.py makemessages --all

Then you should edit the .po files providing proper translations and then run the following for compiling the messages:

    python manage.py compilemessages

Note: You may need to restart the django server for changes to take effect.
