# Change Log
All enhancements and patches to cookiecutter-django will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

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
