.. _sass-compilation-live-reload:

Sass Compilation & Live Reloading
=================================

If you'd like to take advantage of `live reload`_ and Sass compilation:

- Make sure that nodejs_ is installed. Then in the project root run::

    $ npm install

.. _nodejs: http://nodejs.org/download/

- Now you just need::

    $ npm run dev

The base app will now run as it would with the usual ``manage.py runserver`` but with live reloading and Sass compilation enabled.
When changing your Sass files, they will be automatically recompiled and change will be reflected in your browser without refreshing.

To get live reloading to work you'll probably need to install an `appropriate browser extension`_

.. _live reload: http://livereload.com/
.. _appropriate browser extension: http://livereload.com/extensions/
