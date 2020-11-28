Security
========

.. index:: Security, Configuration, TLS, SSL, Encrpytion, Compatibility

Overview
--------

There is a reasonable level of security for most use cases configured as standard in cookiecutter-django, as much as is possible without knowing the features of the website you are building. That being said, your security requirements may differ greatly; before any deployment **you should ensure the security of your website is appropriate for your use case**. As a starting point, you should check any security settings used in cookiecutter-django and see if they are right for you, also actioning any TODOs. A good place to start is `config/settings/production.py`_, as well as `compose/production/traefik/traefik.yml`_ if you are using Docker. Naturally if you collect sensitive data, or have reason to believe your site is at all likely be targeted by hackers, a complete security review before allowing any user access is a must.

.. _`config/settings/production.py`: https://github.com/pydanny/cookiecutter-django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/config/settings/production.py
.. _`compose/production/traefik/traefik.yml`: https://github.com/pydanny/cookiecutter-django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/compose/production/traefik/traefik.yml



Security Checklist
---------------------------------
This list is by no means comprehensive, but is a good starting point for those less well-versed in website security:

- Run ``python manage.py check --deploy`` and ensure any issues listed are fixed (make sure you are checking the production settings by setting ``DJANGO_SETTINGS_MODULE=config.settings.production`` in the environment). Note: if you are using Docker, some settings flagged as missing by Django may be managed by Traefik's config.
- Test your SSL security `using SSL Labs`_, a full score may be overkill and will likely cause compatibility issues with older browsers, but try to action anything flagged in red. **Note**: full marks here does not necessarily make your website 'secure', this tool merely tests the strength of your TLS encryption settings.
- Check how your site stacks up against Mozilla's `Web Security Cheat Sheet`_. Again, completing everything listed here may be overkill but it is good as a reference.
- Consider creating a `Content Security Policy`_ for your site. In short, this is a HTTP header that instructs client browsers where they should load resources from (scripts, stylesheets etc.), and what web features should be enabled (inline HTML script  and style tags, allowed domains for JavaScript AJAX fetches etc.). An ideal policy is to disable everything by default then just enable the features you use on your site.

.. _`using SSL Labs`: https://www.ssllabs.com/ssltest/
.. _`Web Security Cheat Sheet`: https://infosec.mozilla.org/guidelines/web_security.html#web-security-cheat-sheet
.. _`Content Security Policy`: https://content-security-policy.com/

Compatibility Issues
--------------------
By default, cookiecutter-django uses security settings that may break compatibility with very old browsers. Before changing your settings to allow for these older browsers, consider asking your clients to update. There is a trade-off between security and compatibility, and weakening your security to support a minority of users can make things less safe for those who are up to date.

Some settings of note when using Docker (in `compose/production/traefik/traefik.yml`_):

- ``tls.options.default.minVersion: VersionTLS12``: `TLS 1.2 supported browsers`_
- ``tls.options.default.sniStrict: true``: `SNI supported browsers`_
- ``tls.options.default.cipherSuites``: only ECDHE ciphers are used, this will not work in old browsers. Internet Explorer <11 does not work and IE11 seems to only work on Windows 10. Edge is fine though, and is a better alternative for Windows users.

.. _`TLS 1.2 supported browsers`: https://caniuse.com/tls1-2
.. _`SNI supported browsers`: https://caniuse.com/sni

Useful Links
------------
- `Django Deployment Checklist`_
- `SSL and TLS Deployment Best Practices`_
- `Content Security Policy (CSP) Quick Reference Guide`_
- `Mozilla Web Security Cheat Sheet`_

.. _`Django Deployment Checklist`: https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
.. _`SSL and TLS Deployment Best Practices`: https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices
.. _`Content Security Policy (CSP) Quick Reference Guide`: https://content-security-policy.com/
.. _`Mozilla Web Security Cheat Sheet`: https://infosec.mozilla.org/guidelines/web_security.html#web-security-cheat-sheet
