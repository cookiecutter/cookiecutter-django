# Change Log
All enhancements and patches to cookiecutter-django will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [2015-09-14]
### Removed
- Remove unused generated CSS styles (@audreyr)

### Changed
- Use Bootstrap margin utility class `m-b-lg` and remove our custom `navbar-header` class (@audreyr)
- Update Hitch requirements (@audreyr)

## [2015-09-13]
### Removed
- Styles that already exist in Bootstrap 4 (or 3) (@audreyr)

### Changed
- Fix issue #296 - change login.html to use [get_providers](https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/templatetags/socialaccount.py#L84-L93) templatetag because ``allauth.socialaccount`` context processor now is [deprecated](http://django-allauth.readthedocs.org/en/latest/changelog.html#from-0-21-0) (@luzfcb)

## [2015-09-09]
### Added
- post_gen_hook to generate a secret key for use in locals.py. You should define your own for production (@pydanny)

## [2015-09-09]
### Added
- htmlcov to gitignore (@pydanny)

## [2015-09-04]
### Added
- Easy deploy Heroku button and app.json file (@bogdal)

## [2015-09-03]
### Added
- For security reasons, we set explicitly the list of allowed hosts (@bogdal)

## [2015-08-31]
### Removed
- Dokku in favor of docker-compose and other modern Django tools (@pydanny)

## [2015-08-30]
### Changed
- Moved from Bootstrap 3 to Bootstrap 4 (@audreyr)
- Slight Reorganization of the README docs (@pydanny)
- Dokku docs are out of the README and in the docs folder (@pydanny)
- Small improvements in ``install_python_dependencies.sh`` and ``install_os_dependencies.sh`` scripts (@luzfcb)
- Update version of django-crispy-forms, django-extensions, django-test-plus, gevent, coverage, hitchpython and hitchtest (@luzfcb)
- Update AngularJS version to 1.4.4 (@luzfcb)
- Update the usage example on README (@luzfcb)

## [2015-08-28]
### Changed
- Switched to django-mailgun-redux so mail doesn't blow up on Python 3 (@pydanny)


## [2015-08-27]
### Changed
- Grunt Updates: use libsass, add postcss (@288)

## [2015-08-20]
### Changed
- requirements files to match current dependency versions (@pydanny)

## [2015-08-18]
### Added
- Docker support and docker-compose (@jayfk)

## [2015-08-12]
### Added
- hitch for end-to-end testing functionality (@crdoconnor)

## [2015-08-09]
### Added
- test coverage, bringing it to 100% (@pydanny)

## 2015-08-08
### Added
- Gitter badge (@pydanny)
### Changed
- Refactor of cookiecutter-django render tests (@burhan)

## [2015-08-06]
### Added
- More test coverage, up to 97% (@pydanny)
- Slight optimization to celery configuration (@jayfk)

## [2015-08-05]
### Added
- Sentry support (@burhan)

### Changed
- Made the user object python 2 and 3 friendly (@pydanny)
- When using maildump, pin gevent. (@audreyr)
- Updated coverage version. (@audreyr)


## [2015-08-04]
### Added
- Better specification of migrations in .coveragerc. (@audreyr)

## [2015-08-03]
### Added
- Instructions for using coverage and generating reports (@audreyr)
- Coverage project-level config file (@audreyr)
- factory-boy package for improved testing  (@pydanny)
- Error message for duplicate usernames in `users.admin.MyUserCreationForm` (@pydanny)
- Tests on `users.admin.MyUserCreationForm` (@pydanny)

### Changed
- update django-all-auth to 0.23.0  (@pydanny)
- update django-test-plus to 1.0.7  (@pydanny)

### Removed
- Unnecessary users/forms.py module (@pydanny)

## [2015-07-30]
### Changed
- update django-floppyforms version to 1.5.2

## [2015-07-29]
### Removed
- Removed legacy permalink decorator from the users.User model. (@pydanny)

## [2015-07-27]
### Removed
- removed django-allauth template context processors because is deprecated now. see: https://github.com/pennersr/django-allauth/commit/634f4fe60e67c266aadcfba2981074f005db340c (@burhan)

### Changed
- update version of ipython, django-allauth (@luzfcb)
- update version of django-braces, django-floppyforms, django-model-utils (#287)(@burhan)

## [2015-07-21]
### Changed
- memcached is as a cache is replace with redis (#258)(@burhan)

## [2015-07-18]
### Changed
- Heroku deployment docs (@stepmr)
    - Heroku's free postgres tier is now "hobby-dev"
    - pg:backups require a scheduled time
    - add missing Mailgun API key
    - Django recommends setting the PYTHONHASHSEED environment variable to random. See: https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/#python-options
    - Use openssl to generate a secure, random secret_key


## [2015-07-17]
### Added
- @models.permalink decorator to User.get_absolute_url() method

### Fixed
- Broken user_form.html (@pydanny)

## [2015-07-16]
### Added
- django-test-plus (@pydanny)
- option use maildump instead of ConsoleEmailHandler (@burhan)
- Changelog.md (@pydanny)

### Fixed
- where 'DEFAULT_FROM_EMAIL' was used to cast the value (@jayfk)

### Removed
- unnecessary header block tag and 'user:' prefix. (@pydanny)
