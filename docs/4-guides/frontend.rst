.. _frontend-guide:

Frontend: htmx and Pico CSS
===========================

Generated projects ship a server-rendered frontend with no Node.js toolchain:

- `htmx`_ adds partial page updates on top of regular links and forms. It is provided by `django-htmx`_, which bundles the htmx script.
- `Pico CSS`_ styles semantic HTML (``<nav>``, ``<article>``, ``<form>``, ``<table>``...) without utility classes. A pinned release is vendored in the project.

Every page works without JavaScript: links keep their ``href`` and forms keep their ``action``, htmx only enhances them.

.. _htmx: https://htmx.org
.. _django-htmx: https://django-htmx.readthedocs.io
.. _Pico CSS: https://picocss.com

Pico CSS
--------

Pico lives in ``<project_slug>/static/vendor/pico/``:

- ``pico.min.css``: the stylesheet, byte-for-byte identical to the upstream release.
- ``LICENSE.md``: the MIT licence of that release.
- ``pico.json``: the vendored version, the upstream source URL, the licence and the SHA-256 checksum of ``pico.min.css``.

The stylesheet is loaded by ``base.html`` through ``{% static 'vendor/pico/pico.min.css' %}``. The vendored files are excluded from pre-commit hooks and from editor clean-ups (see ``.editorconfig``) so the checksum stays valid.

To upgrade Pico:

#. Download ``css/pico.min.css`` and ``LICENSE.md`` from the new tag of the `Pico repository`_ into ``static/vendor/pico/``.
#. Compute the checksum, ``shasum -a 256 pico.min.css``, and update ``version``, ``source`` and ``sha256`` in ``pico.json``.
#. Run the test suite: ``tests/test_vendored_assets.py`` (template) and ``test_vendored_pico_intact`` (generated project) fail when the file and the metadata disagree.

.. _Pico repository: https://github.com/picocss/pico/releases

Project-specific styles go in ``static/css/project.css``, which is loaded after Pico and uses Pico's CSS variables (``--pico-primary``, ``--pico-del-color``...).

htmx
----

``django-htmx`` is installed in ``INSTALLED_APPS`` and its ``HtmxMiddleware`` sets ``request.htmx`` on every request. The script is rendered by ``{% htmx_script %}`` in ``base.html``; when ``DEBUG`` is on it also loads the django-htmx debug extension, which shows Django error pages for failed htmx requests.

CSRF
~~~~

``base.html`` puts Django's CSRF token on the ``<body>`` element so htmx sends it with every request, including ones that are not form submissions:

.. code-block:: html

    <body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>

The ``CsrfViewMiddleware`` stays enabled, so an unsafe request without the header (or without the form's hidden field) is rejected with a 403. This works with ``CSRF_COOKIE_HTTPONLY = True`` because the token comes from the template, not from the cookie.

Partial templates
~~~~~~~~~~~~~~~~~

Views that answer htmx requests with a fragment instead of a full page use ``HtmxTemplateMixin`` from ``<project_slug>/htmx.py``:

.. code-block:: python

    class UserDetailView(LoginRequiredMixin, HtmxTemplateMixin, DetailView):
        model = User
        htmx_template_name = "users/partials/user_detail.html"

The mixin renders ``htmx_template_name`` when the request carries the ``HX-Request`` header and the regular template otherwise, and it adds ``Vary: HX-Request`` to the response so a cache never serves a fragment to a full-page request. Only views whose response differs need the mixin.

The user profile pages show the pattern: the "My Info" button loads the edit form into the profile card with ``hx-get``/``hx-target``/``hx-push-url``, the form posts with ``hx-post``, and after the redirect the profile card is swapped back. The same links and form work as plain full-page navigation when JavaScript is off.

Messages
~~~~~~~~

``partials/messages.html`` renders Django's messages inside ``<div id="messages">``. Partial templates include it too, marked with ``hx-swap-oob="true"``, so messages added during an htmx request (for example the "Information successfully updated" notice) are swapped into the page out-of-band.

Forms
-----

Forms are rendered by Django's own form renderer. ``FORM_RENDERER = "django.forms.renderers.TemplatesSetting"`` lets the project override ``django/forms/field.html`` (in ``<project_slug>/templates/django/forms/``), which produces Pico markup: a ``<label>``, the widget, the error list and a ``<small>`` help text. Django adds ``aria-invalid`` and ``aria-describedby`` to widgets with errors, which Pico uses for its validation styles. ``{{ form }}`` is all a template needs; django-allauth's forms go through the same renderer via ``templates/allauth/elements/fields.html``.
