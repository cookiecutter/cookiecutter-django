Cookiecutter Vue Django
=======================

.. image:: https://travis-ci.com/ilikerobots/cookiecutter-vue-django.svg?branch=master
    :target: https://travis-ci.com/ilikerobots/cookiecutter-vue-django?branch=master
    :alt: Build Status

.. image:: https://readthedocs.org/projects/cookiecutter-vue-django/badge/?version=latest
    :target: https://cookiecutter-vue-django.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ilikerobots/cookiecutter-vue-django/shield.svg
    :target: https://pyup.io/repos/github/ilikerobots/cookiecutter-vue-django/
    :alt: Updates

Vue + Django with no compromise. 

Cookiecutter Vue Django is a framework for jumpstarting production-ready Django + Vue projects quickly.  Expanding on the wonderful Cookiecutter Django, this project template allows the intermingling of both Django Templates and Vue, even on the same page, without compromising the full power of either. 

Typical solutions to integrating Django and Vue forgo much of the strengths of one lieu of the other. For example, a common approach is using Django Rest Framework as backend and writing the entire front end in Vue, making it difficult to utilize Django templates in places it could be expedient. A second approach is to use Vue within Django templates using browser `<script>` includes, but then lost is the ability to use Vue's Single File Components.

This project utilizes a different approach, melding these two technologies more naturally. As a result, not only are the typical compromises eliminated, but additional distinct advantages are realized:

* Increased flexibility: The developer is free to use Django Templates or Vue as appropriate, choosing the right tool for the job
* Increased development speed: Reduce time spent fighting the framework by using Django and Vue where each excels
* Increased performance: Leverage Django's powerful caching backend to deliver content-rich pages quickly with little or no Javascript, while deferring complex and interactive Vue functionality until after page load

Features
---------

* All the features of the amazing cookiecutter-django_ 
* Harmonious coexistence of Django templates and Vue components
* Vue Single File Components (SFCs)
* Multi-page App (MPA) layout
* Vue Loader Hot Reload
* Property passing from Django Template -> Vue Component
* Sass/SCSS pre-compilation of Vue Components
* Vue DevTools support
* Chunked resource loading via webpack
* Deferred loading of Vue and/or Vue components
* Shared Vuex state across components on the same page
* Persistent state across page loads
* REST support via Axios -> DRF 
* Sample application illustrating all of the above

.. _cookiecutter-django: https://github.com/pydanny/cookiecutter-django

Usage
------

First, get Cookiecutter. Trust me, it's awesome::

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo::

    $ cookiecutter https://github.com/ilikerobots/cookiecutter-vue-django


You'll be prompted for some values. Provide them, then a Django project will be created for you. Don't forget to carefully look at the generated README.

For more detailed instructions, see upstream cookiecutter-django_

.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _cookiecutter-django: https://github.com/pydanny/cookiecutter-django

Issues
-----------

* If you think you found a bug or want to request a feature, please open an issue_.

.. _`issue`: https://github.com/ilikerobots/cookiecutter-vue-django/issues

Articles
---------

This cookiecutter is based on the methods described in the following articles

* `Vue + Django — Best of Both Frontends`_ - 26 May 2019 by Mike Hoolehan
* `Vue + Django — Best of Both Frontends, Part 2`_ - 4 Dec 2019, id
* `Django + Vue — Blazing Content, Rich Interactivity`_ - 23 Apr 2020, id

.. _`Vue + Django — Best of Both Frontends`: https://medium.com/js-dojo/vue-django-best-of-both-frontends-701307871478
.. _`Vue + Django — Best of Both Frontends, Part 2`: https://medium.com/js-dojo/django-vue-vuex-best-of-both-frontends-part-2-1dcb78215575
.. _`Django + Vue — Blazing Content, Rich Interactivity`: https://medium.com/js-dojo/django-vue-blazing-content-rich-interactivity-b34e45d8c602


Show your Support
-----------------

If you find this repository useful, then please consider leaving a star so this project can reach more people. Also, if the articles above were helpful, then a clap on those platforms would also be appreciated.  Thanks!


Code of Conduct
---------------

Everyone interacting in the this project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.


.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/
