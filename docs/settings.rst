Settings
==========

This project relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps environment variables to their Django setting:


======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_ADMIN_URL                        n/a                         r'^admin/'                                     raises error
DJANGO_CACHES                           CACHES (default)            locmem                                         redis
DJANGO_DATABASES                        DATABASES (default)         See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_SECURE_BROWSER_XSS_FILTER        SECURE_BROWSER_XSS_FILTER   n/a                                            True
DJANGO_SECURE_SSL_REDIRECT              SECURE_SSL_REDIRECT         n/a                                            True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF      SECURE_CONTENT_TYPE_NOSNIFF n/a                                            True
DJANGO_SECURE_FRAME_DENY                SECURE_FRAME_DENY           n/a                                            True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS   HSTS_INCLUDE_SUBDOMAINS     n/a                                            True
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
DJANGO_DEFAULT_FROM_EMAIL               DEFAULT_FROM_EMAIL          n/a                                            "your_project_name <noreply@your_domain_name>"
DJANGO_SERVER_EMAIL                     SERVER_EMAIL                n/a                                            "your_project_name <noreply@your_domain_name>"
DJANGO_EMAIL_SUBJECT_PREFIX             EMAIL_SUBJECT_PREFIX        n/a                                            "[your_project_name] "
DJANGO_ALLOWED_HOSTS                    ALLOWED_HOSTS               ['*']                                          ['your_domain_name']
======================================= =========================== ============================================== ======================================================================

The following table lists settings and their defaults for third-party applications, which may or may not be part of your project:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
DJANGO_SENTRY_DSN                       SENTRY_DSN                  n/a                                            raises error
DJANGO_SENTRY_CLIENT                    SENTRY_CLIENT               n/a                                            raven.contrib.django.raven_compat.DjangoClient
DJANGO_SENTRY_LOG_LEVEL                 SENTRY_LOG_LEVEL            n/a                                            logging.INFO
DJANGO_MAILGUN_API_KEY                  MAILGUN_ACCESS_KEY          n/a                                            raises error
DJANGO_MAILGUN_SERVER_NAME              MAILGUN_SERVER_NAME         n/a                                            raises error
MAILGUN_SENDER_DOMAIN                   MAILGUN_SENDER_DOMAIN       n/a                                            raises error
NEW_RELIC_APP_NAME                      NEW_RELIC_APP_NAME          n/a                                            raises error
NEW_RELIC_LICENSE_KEY                   NEW_RELIC_LICENSE_KEY       n/a                                            raises error
DJANGO_OPBEAT_APP_ID                    OPBEAT['APP_ID']            n/a                                            raises error
DJANGO_OPBEAT_SECRET_TOKEN              OPBEAT['SECRET_TOKEN']      n/a                                            raises error
DJANGO_OPBEAT_ORGANIZATION_ID           OPBEAT['ORGANIZATION_ID']   n/a                                            raises error
======================================= =========================== ============================================== ======================================================================

--------------------------
Other Environment Settings
--------------------------

DJANGO_ACCOUNT_ALLOW_REGISTRATION (=True)
    Allow enable or disable user registration through `django-allauth` without disabling other characteristics like authentication and account management. (Django Setting: ACCOUNT_ALLOW_REGISTRATION)
