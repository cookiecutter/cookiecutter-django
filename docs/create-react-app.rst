ReactJS with Live Reloading
===========================

If you'd like to take take advantage of ReactJS to develop your UI:

- Start Django server in the project root run:

    $ python manage.py runserver

- Make sure that yarn_ is installed.  Then in a second terminal, run the following in the project root::

    $ cd frontend
    $ yarn install
    $ yarn build

.. _yarn: https://yarnpkg.com/lang/en/docs/install/

- Start React UI::

    $ yarn start

This will automatically open a browser with your react app.
Now you can open App.js and make changes and you should see it reload changes to the UI automatically!
