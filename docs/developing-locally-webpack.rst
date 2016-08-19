Developing Locally with Webpack
===============================

.. index:: Webpack, React, Redux, Karma, HMR

The steps below will get you up and running with a super speedy local development environment with Webpack, React, Redux and Hot module Replacement.

Before you begin, make sure you've created a python virtual environment, installed local python dependencies and created a postgres database::

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements/local.txt
    $ createdb [project_slug]
    $ python manage.py migrate
    $ python manage.py runserver

These prerequisite steps are detailed more in the `developing locally section`_. If you've already done them, continue to installing javascript dependencies.

.. _developing locally section: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html


Install javascript dependencies
-------------------------------

You will need `NodeJS`_ set up on your local machine to use `npm`_.

.. _NodeJS: https://nodejs.org/en/
.. _npm: https://www.npmjs.com/


Install all the javascript dev dependencies as specified in the ``.package.json`` file::

    $ npm install


Start the django and webpack servers
------------------------------------

Start up the python and webpack dev server's::

    $ npm start


Open up ``http://localhost:8000`` to see the project running in your browser.

You can also open ``http://localhost:8080`` to see the webpack-dev-server running.

**Why are there two servers? Why not use django's built in static file server?**

We are using webpack's dev server to enable `hot module replacement`_.

If you're not familiar with hmr, then try editing one of the react components that was generated in your static directory.
You will see your updates without any page reloading.
Because we have sass loaders in our webpack configuration, this also applies to style edits.

.. _hot module replacement: https://webpack.github.io/docs/hot-module-replacement.html


**Static Project Structure**

The static project is in your django project's static root, specifically: ``[ project_slug ]/static/[ project_slug ]``.

There is also a generated ``README.md`` in that directory that outlines the React + Redux + Webpack project structure.


Running Tests with karma
------------------------

Javascript tests are in the ``[ project_slug ]/static/[ project_slug ]/__tests__/`` directory.

To run karma::

    $ npm test

This will also run eslint on your javascript files because it is a loader in the webpack test config.

To keep karma running and watch for file changes run::

    $ npm watch:test


Deployment with webpack
-----------------------

To build your assets for production deployment::

    $ npm run build

This will bundle all your files and place them in the ``[ project_slug ]/static/[ project_slug ]/dist/`` directory as specified in the webpack production config's ``output.path``.

There is a generated ``webpack-stats-production.json`` file that contains references to webpack's built files that django will need in production. It is ignored by git but you will want to make sure it is included in deployment.


Bundling static assets
----------------------

You can "bundle" (webpack term) all your static assets into separate modules for each page. When webpack bundles these assets it looks for entry points that you specify (in ``config.entry``) and loads all that entry points dependencies into the bundle, if that entry point has dependencies, webpack will load those dependencies and so on recursively. You can even include image files and style sheets as dependencies too.

The current webpack configuration that is built in the django-cookiecutter project is already configured to create three bundles, ``main``, ``vendor`` and ``common``.

* ``main`` contains the main project app, currently a counter demo.
* ``vendor`` contains all the third party code, currently react, redux and related libraries. We isolate ``vendor`` because it is likely to be shared between apps and will also not be updated in production as much as our ``main`` bundle so it can stay cached.
* ``common`` contains shared modules between bundles.

These bundles are being served locally by the webpack-development-server when you run ``npm start``.

Bundles need to be included in django templates. Bundles are hashed each build though, so you can't just add a script tag for them.
We use ``django-webpack-loader`` to make Django aware of webpack's build stats. In templates, we can use tags provided by ``django-webpack-loader`` to reference each bundle with the correct build hash.

.. code-block:: django

    <!--base.html-->
    {% load render_bundle from webpack_loader %}
    ...
    {% block javascript %}
    <!-- render 'main' bundle with correct build hash -->
    {% render_bundle 'main' %}
    {% endblock javascript %}

**Bundling Example:**

Say we create a new module for user administration. We don't want to include it in the main app because it's only needed in the user page.

We would first create a seperate entry point in our ``./config/webpack.base.config.js`` file:

.. code-block:: javascript

    entry: {
        main: './assets/js/index',  // the entry that already exists for our main app
        users: './assets/js/userApp', // create a new entry for our userApp called 'users'
    }


Then we can load that bundle in our ``users.html`` template:

.. code-block:: django

    <!--users.html-->
    {% load render_bundle from webpack_loader %}
    ...
    {% block javascript %}
    {{ block.super }}
    {% render_bundle 'users' %}
    {% endblock javascript %}
