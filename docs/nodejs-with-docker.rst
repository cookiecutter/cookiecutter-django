Node.js with Docker
===================

.. index:: node, nodejs, docker, docker-compose

`Node.js`_ support is provided out-of-the-box, ready for use as-is, or with any kind of customizations suiting the specific needs of the project.

.. _`Node.js`: https://nodejs.org/en/

*All paths are relative to the generated project's root.*


.. _nodewithdocker-prereq:

Prerequisites
-------------

- The project was generated with :code:`use_docker` set to :code:`y`.
- These :ref:`devlocdocker-prereq` are met as well.


.. _nodewithdocker-overview:

Overview
--------

Essential aspects of Node.js integration are

- node docker-compose service (:code:`node`) definition in :code:`./dev.yml`;
- :code:`./compose/node/Dockerfile-dev` defining the :code:`node` image;
- :code:`./node_modules/` 'overlayed' with :code:`/app/node_modules/`, its counterpart from the running instance of :code:`node`.


Workflow
--------

#. [*skip if done*] :ref:`devlocdocker-build-the-stack`:
    - when building :code:`node` image from scratch, dependencies from :code:`package.json` are installed.
#. :ref:`devlocdocker-boot-the-system`.

To log the running :code:`node` container's activity,

.. code-block:: bash

    $ docker-compose -f dev.yml logs node
