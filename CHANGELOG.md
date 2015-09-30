# Change Log
All enhancements and patches to cookiecutter-django will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [2015-09-30]
### Changed
- Fixed Sentry logging with celery (@jayfk)
- Added pep8 and pyflakes to requirements (@jayfk)
- Fixed url() arguments in urls.py because String view arguments to url() is deprecated in django 1.9 (@siauPatrick)
- Update version of cookiecutter, coverage, django-environ, django-extensions, hitchpython, hitchselenium, hitchserve, pytest, pytz, whitenoise (@luzfcb)
- Update the usage example in README (@luzfcb)
- Update 'now' date in cookiecutter.json (@luzfcb)

## [2015-09-29]
### Changed
- Fix RST in Docker docs (@andor-pierdelacabeza)

## [2015-09-27]
### Added
- Added advice on how to persist changes with boot2docker (@jayfk)

###Changed
- Removed duplicate from `CONTRIBUTORS.rst` (@jayfk)

## [2015-09-26]
### Added
- Add .pylintrc and .pep8 (@kaidokert)

### Changed
- Move pep8 rules to setup.cfg (@audreyr)
- Better pep8 rules for exclusion (@audreyr)
- Document all linters (@audreyr)
- Sass linting and improvements to alerts (@audreyr)

## [2015-09-25]
### Changed
- django-mailgun requirement to 0.7.2 (@pydanny)
- Remove commented-out flake8 ignore rule. (@audreyr)

## [2015-09-24]
### Changed
- Add user-uploaded media dir to .gitignore (@audreyr)
- Update .editorconfig to use 2 spaces for html, css, scss, json (@audreyr)
- Have flake8 ignore node_modules dir (@audreyr)

## [2015-09-23]
### Changed
- Add workaround for django-debug-toolbar conflict with Bootstrap 4 (@audreyr)

## [2015-09-22]
### Added
- Add Python version option for deployment (@yunti)

## [2015-09-21]
### Changed
- django-mailgun-redux to django-mailgun, because @pydanny now has commit rights
### Removed
- Excess "loggers" from LOGGING setting (@siauPatrick)

## [2015-09-18]
### Changed
- Major reorganization of docs (@pydanny)
- Fix expanded navbar on mobile (@jayfk)
- Update various requirements (@audreyr)

## [2015-09-17]
### Added
- Fix for wsgi.py for Raven in dev (@yunti)

## [2015-09-15]
### Added
- whitespace to allow proper rendering of RST (@IanLee1521 )

## [2015-09-14]
### Added
- Functionality to delete taskapp if celery isn't going to be used (@pydanny)

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
