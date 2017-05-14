Gulp with Docker
================

.. index:: gulp, gulpjs, gulpfile, gulpfilejs, docker, docker-compose

`Gulp`_ support is provided out-of-the-box, ready for use as-is, or with any kind of customizations suiting the specific needs of the project.

.. _`Gulp`: http://gulpjs.com/

*All paths are relative to the generated project's root.*


Prerequisites
-------------

- These :ref:`nodewithdocker-prereq` are satisfied.


Overview
--------

:ref:`nodewithdocker-overview` Node.js integration details first to get the whole picture.

Essential aspects of Gulp integration are

- :code:`./gulpfile.js` with Gulp tasks defined;
- :code:`./{{ cookiecutter.project_slug }}/static/build/` (build directory) with static assets built via Gulp.

Let us take a closer look at :code:`./gulpfile.js`:

- paths to static assets are provided by :code:`pathsConfig()`;
- for clarity, related tasks are grouped by :code:`region`:
    - :code:`images`:
        - :code:`images`: run image-related tasks in parallel, namely:
            - :code:`favicons-images`: process favicon images only;
            - :code:`nonfavicons-images`: process all images except for favicons.
    - :code:`scripts`:
        - :code:`scripts`: run script-related tasks in sequence, namely:
            - :code:`js-scripts`: process js scripts.
    - :code:`styles`:
        - :code:`styles`: run script-related tasks in sequence, namely:
            - :code:`sass-styles`: process SCSS styles;
            - :code:`css-styles`: process CSS styles.
    - :code:`build`:
        - :code:`build`: run :code:`images`, :code:`scripts`, and :code:`styles` in parallel;
        - :code:`clean-build`: clean up build directory:
- the :code:`default` task runs the following ones in sequence:
    - :code:`build`;
    - :code:`init-browserSync`: initialize `BrowserSync`_;
    - :code:`watch`: watch static asset files/directories changes, running BrowserSync on any changes.

.. _`BrowserSync`: https://www.browsersync.io/


Workflow
--------

#. [*skip if done*] :ref:`devlocdocker-build-the-stack`;
#. :ref:`devlocdocker-boot-the-system`.

By default, :code:`gulp` command gets executed immediately after :code:`node`
container startup (see :code:`./dev.yml` for details) which in turn invokes
the :code:`default` task, so generally one would not need to run any
of the aforementioned tasks manually. However, should the need arise,
oftentimes just a few of the tasks listed above will be used to, for instance,
straightforwardly :code:`build` all assets

.. code-block:: bash

    $ docker-compose -f dev.yml exec node gulp build

or build :code:`scripts` selectively

.. code-block:: bash

    $ docker-compose -f dev.yml exec node gulp scripts
