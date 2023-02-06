If your email server used to send email isn't configured properly (Mailgun by default),
attempting to send an email will cause an Internal Server Error.

By default, ``django-allauth`` is setup to `have emails verifications mandatory`_,
which means it'll send a verification email when an unverified user tries to
log-in or when someone tries to sign-up.

This may happen just after you've setup your Mailgun account, which is running in a
sandbox subdomain by default. Either add your email to the list of authorized recipients
or verify your domain.


.. _have emails verifications mandatory: https://django-allauth.readthedocs.io/en/latest/configuration.html?highlight=ACCOUNT_EMAIL_VERIFICATION
