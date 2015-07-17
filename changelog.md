# Change Log
All enhancements and patches to cookiecutter-django will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

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
