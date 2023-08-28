# Change Log
All enhancements and patches to Cookiecutter Django will be documented in this file.

<!-- GENERATOR_PLACEHOLDER -->

## 2023.08.19


### Changed

- Override `_after_postgeneration` to force save in `UserFactory` ([#4534](https://github.com/cookiecutter/cookiecutter-django/pull/4534))

## 2023.08.17


### Updated

- Update argon2-cffi to 23.1.0 ([#4527](https://github.com/cookiecutter/cookiecutter-django/pull/4527))

- Auto-update pre-commit hooks ([#4530](https://github.com/cookiecutter/cookiecutter-django/pull/4530))

## 2023.08.16


### Updated

- Update django-upgrade to 1.14.1 ([#4528](https://github.com/cookiecutter/cookiecutter-django/pull/4528))

## 2023.08.15


### Updated

- Update redis to 5.0.0 ([#4526](https://github.com/cookiecutter/cookiecutter-django/pull/4526))

## 2023.08.14


### Changed

- Install Django and DRF stubs with `compatible-mypy` extra (as per offical recommendation) ([#4361](https://github.com/cookiecutter/cookiecutter-django/pull/4361))

-  Fix `overrideCommand` value in `devcontainer` so that the `django` container can run (#4517) ([#4517](https://github.com/cookiecutter/cookiecutter-django/pull/4517))

### Fixed

- Prevent error in data migration caused by long project name ([#4525](https://github.com/cookiecutter/cookiecutter-django/pull/4525))

- Remove unused gulp-concat when Webpack is selected ([#4520](https://github.com/cookiecutter/cookiecutter-django/pull/4520))

- Exclude env files from container image (add .envs/ to .dockerignore) ([#4476](https://github.com/cookiecutter/cookiecutter-django/pull/4476))

### Updated

- Update werkzeug to 2.3.7 ([#4521](https://github.com/cookiecutter/cookiecutter-django/pull/4521))

- Update coverage to 7.3.0 ([#4516](https://github.com/cookiecutter/cookiecutter-django/pull/4516))

- Update django-debug-toolbar to 4.2.0 ([#4511](https://github.com/cookiecutter/cookiecutter-django/pull/4511))

- Update flower to 2.0.1 ([#4518](https://github.com/cookiecutter/cookiecutter-django/pull/4518))

## 2023.08.10


### Fixed

- Corrected &#39;or&#39; translation to pt-br ([#4507](https://github.com/cookiecutter/cookiecutter-django/pull/4507))

## 2023.08.04


### Updated

- Auto-update pre-commit hooks ([#4503](https://github.com/cookiecutter/cookiecutter-django/pull/4503))

## 2023.08.01


### Updated

- Auto-update pre-commit hooks ([#4499](https://github.com/cookiecutter/cookiecutter-django/pull/4499))

- Update django-anymail to 10.1 ([#4497](https://github.com/cookiecutter/cookiecutter-django/pull/4497))

- Update sentry-sdk to 1.29.2 ([#4496](https://github.com/cookiecutter/cookiecutter-django/pull/4496))

- Update django to 4.2.4 ([#4495](https://github.com/cookiecutter/cookiecutter-django/pull/4495))

- Update flake8 to 6.1.0 ([#4489](https://github.com/cookiecutter/cookiecutter-django/pull/4489))

- Update uvicorn to 0.23.2 ([#4490](https://github.com/cookiecutter/cookiecutter-django/pull/4490))

- Update sentry-sdk to 1.29.1 ([#4494](https://github.com/cookiecutter/cookiecutter-django/pull/4494))

## 2023.07.30


### Fixed

- Fix `README.md` file extension in `setup.py` ([#4488](https://github.com/cookiecutter/cookiecutter-django/pull/4488))

## 2023.07.28


### Changed

- Add support for Drone CI ([#4382](https://github.com/cookiecutter/cookiecutter-django/pull/4382))

## 2023.07.27


### Documentation

- Document that `docker exec` does not work for running management commands ([#4487](https://github.com/cookiecutter/cookiecutter-django/pull/4487))

- Add Webpack instructions for developping locally with HTTPS ([#4486](https://github.com/cookiecutter/cookiecutter-django/pull/4486))

## 2023.07.25


### Updated

- Upgrade to traefik 2.10.4 ([#4483](https://github.com/cookiecutter/cookiecutter-django/pull/4483))

## 2023.07.24


### Fixed

- Add missing custom CRSF error page in prod ([#4464](https://github.com/cookiecutter/cookiecutter-django/pull/4464))

### Documentation

- Replace `docker-compose` by `docker compose` in docs ([#4463](https://github.com/cookiecutter/cookiecutter-django/pull/4463))

### Updated

- Update drf-spectacular to 0.26.4 ([#4481](https://github.com/cookiecutter/cookiecutter-django/pull/4481))

## 2023.07.20


### Updated

- Update djlint to 1.32.1 ([#4475](https://github.com/cookiecutter/cookiecutter-django/pull/4475))

## 2023.07.19


### Updated

- Update factory-boy to 3.3.0 ([#4472](https://github.com/cookiecutter/cookiecutter-django/pull/4472))

- Update gunicorn to 21.2.0 ([#4473](https://github.com/cookiecutter/cookiecutter-django/pull/4473))

- Update djlint to 1.32.0 ([#4471](https://github.com/cookiecutter/cookiecutter-django/pull/4471))

## 2023.07.18


### Updated

- Update gunicorn to 21.1.0 ([#4470](https://github.com/cookiecutter/cookiecutter-django/pull/4470))

- Update uvicorn to 0.23.1 ([#4468](https://github.com/cookiecutter/cookiecutter-django/pull/4468))

- Update gunicorn to 21.0.1 ([#4466](https://github.com/cookiecutter/cookiecutter-django/pull/4466))

## 2023.07.13


### Updated

- Update sentry-sdk to 1.28.1 ([#4458](https://github.com/cookiecutter/cookiecutter-django/pull/4458))

## 2023.07.11


### Changed

- Improve type hints for `UserSerializer` ([#4429](https://github.com/cookiecutter/cookiecutter-django/pull/4429))

- [pre-commit.ci] pre-commit autoupdate ([#4453](https://github.com/cookiecutter/cookiecutter-django/pull/4453))

### Fixed

- Fix `/tmp` bind mount in devcontainer config ([#4455](https://github.com/cookiecutter/cookiecutter-django/pull/4455))

### Updated

- Update black to 23.7.0 ([#4452](https://github.com/cookiecutter/cookiecutter-django/pull/4452))

## 2023.07.10


### Fixed

- Prevent user&#39;s name being shown twice on user details page if username is set to email ([#4436](https://github.com/cookiecutter/cookiecutter-django/pull/4436))

- Add missing trailing space in `EMAIL_SUBJECT_PREFIX` setting ([#4434](https://github.com/cookiecutter/cookiecutter-django/pull/4434))

### Documentation

- Clarify documentation on which port to use to access the application when using Webpack or Gulp ([#4413](https://github.com/cookiecutter/cookiecutter-django/pull/4413))

### Updated

- Update django-coverage-plugin to 3.1.0 ([#4446](https://github.com/cookiecutter/cookiecutter-django/pull/4446))

- Update pillow to 10.0.0 ([#4432](https://github.com/cookiecutter/cookiecutter-django/pull/4432))

- Update django-cors-headers to 4.2.0 ([#4445](https://github.com/cookiecutter/cookiecutter-django/pull/4445))

- Update sentry-sdk to 1.28.0 ([#4444](https://github.com/cookiecutter/cookiecutter-django/pull/4444))

## 2023.07.09


### Fixed

- Fix missing run configurations when PyCharm is selected ([#4441](https://github.com/cookiecutter/cookiecutter-django/pull/4441))

## 2023.07.08


### Updated

- Update sentry-sdk to 1.27.1 ([#4440](https://github.com/cookiecutter/cookiecutter-django/pull/4440))

## 2023.07.04


### Changed

- Add PostgreSQL 15 ([#4431](https://github.com/cookiecutter/cookiecutter-django/pull/4431))

- [pre-commit.ci] pre-commit autoupdate ([#4438](https://github.com/cookiecutter/cookiecutter-django/pull/4438))

### Updated

- Update sentry-sdk to 1.27.0 ([#4439](https://github.com/cookiecutter/cookiecutter-django/pull/4439))

- Update postcss-preset-env to 9.0.0 ([#4437](https://github.com/cookiecutter/cookiecutter-django/pull/4437))

## 2023.07.03


### Changed

- Add a devcontainer configuration with Docker ([#4198](https://github.com/cookiecutter/cookiecutter-django/pull/4198))

### Updated

- Update django-stubs to 4.2.3 ([#4430](https://github.com/cookiecutter/cookiecutter-django/pull/4430))

- Update django to 4.2.3 ([#4435](https://github.com/cookiecutter/cookiecutter-django/pull/4435))

## 2023.06.30


### Changed

- Add option to use django-allauth workflow in the admin ([#1921](https://github.com/cookiecutter/cookiecutter-django/pull/1921))

## 2023.06.29


### Changed

- Replace psycopg2 by psycopg3 ([#4421](https://github.com/cookiecutter/cookiecutter-django/pull/4421))

## 2023.06.28


### Changed

- Upgrade to django 4.2 ([#4393](https://github.com/cookiecutter/cookiecutter-django/pull/4393))

### Fixed

- Fix PostgreSQL version in GitHub workflow ([#4423](https://github.com/cookiecutter/cookiecutter-django/pull/4423))

### Updated

- Update werkzeug to 2.3.6 ([#4427](https://github.com/cookiecutter/cookiecutter-django/pull/4427))

- Update django-compressor to 4.4 ([#4422](https://github.com/cookiecutter/cookiecutter-django/pull/4422))

## 2023.06.27


### Changed

- Populate User `name` field during social auth ([#3968](https://github.com/cookiecutter/cookiecutter-django/pull/3968))

- Add djLint for HTML formatting and linting ([#4389](https://github.com/cookiecutter/cookiecutter-django/pull/4389))

### Fixed

- Only include prettier pre-commit hook with node-based front-end pipeline ([#4418](https://github.com/cookiecutter/cookiecutter-django/pull/4418))

### Updated

- Update djangorestframework-stubs to 3.14.2 ([#4420](https://github.com/cookiecutter/cookiecutter-django/pull/4420))

- Update django-stubs to 4.2.2 ([#4419](https://github.com/cookiecutter/cookiecutter-django/pull/4419))

## 2023.06.26


### Updated

- Update pytest to 7.4.0 ([#4412](https://github.com/cookiecutter/cookiecutter-django/pull/4412))

- Update redis to 4.6.0 ([#4415](https://github.com/cookiecutter/cookiecutter-django/pull/4415))

- Update mypy to 1.4.1 ([#4416](https://github.com/cookiecutter/cookiecutter-django/pull/4416))

## 2023.06.22


### Updated

- Update pygithub to 1.59.0 ([#4410](https://github.com/cookiecutter/cookiecutter-django/pull/4410))

- Update drf-spectacular to 0.26.3 ([#4411](https://github.com/cookiecutter/cookiecutter-django/pull/4411))

- Update sentry-sdk to 1.26.0 ([#4409](https://github.com/cookiecutter/cookiecutter-django/pull/4409))

## 2023.06.21


### Updated

- Upgrade traefik to 2.10.3 ([#4408](https://github.com/cookiecutter/cookiecutter-django/pull/4408))

## 2023.06.19


### Updated

- Auto-update pre-commit hooks ([#4405](https://github.com/cookiecutter/cookiecutter-django/pull/4405))

- Update celery to 5.3.1 ([#4404](https://github.com/cookiecutter/cookiecutter-django/pull/4404))

## 2023.06.18


### Changed

- Fix missing celery env variable when running compilemessages ([#4403](https://github.com/cookiecutter/cookiecutter-django/pull/4403))

### Updated

- Update flower to 2.0.0 ([#4402](https://github.com/cookiecutter/cookiecutter-django/pull/4402))

## 2023.06.17


## 2023.06.16


### Updated

- Update whitenoise to 6.5.0 ([#4400](https://github.com/cookiecutter/cookiecutter-django/pull/4400))

- Update django-redis to 5.3.0 ([#4399](https://github.com/cookiecutter/cookiecutter-django/pull/4399))

- Auto-update pre-commit hooks ([#4395](https://github.com/cookiecutter/cookiecutter-django/pull/4395))

## 2023.06.14


### Updated

- Update django-cors-headers to 4.1.0 ([#4391](https://github.com/cookiecutter/cookiecutter-django/pull/4391))

- Update django-upgrade to 1.14.0 ([#4394](https://github.com/cookiecutter/cookiecutter-django/pull/4394))

- Update django-webpack-loader to 2.0.1 ([#4392](https://github.com/cookiecutter/cookiecutter-django/pull/4392))

- Update pre-commit to 3.3.3 ([#4390](https://github.com/cookiecutter/cookiecutter-django/pull/4390))

## 2023.06.11


### Updated

- Update pytest to 7.3.2 ([#4384](https://github.com/cookiecutter/cookiecutter-django/pull/4384))

- Auto-update pre-commit hooks ([#4385](https://github.com/cookiecutter/cookiecutter-django/pull/4385))

## 2023.06.09


### Fixed

- Fix missing `compilemessages` step before deploying to prod ([#4363](https://github.com/cookiecutter/cookiecutter-django/pull/4363))

## 2023.06.08


### Fixed

- Fix failure in user view test caused by translations ([#4374](https://github.com/cookiecutter/cookiecutter-django/pull/4374))

### Updated

- Update to Python 3.11.4 in production Docker compose ([#4378](https://github.com/cookiecutter/cookiecutter-django/pull/4378))

- Update to Python 3.11.4 in docs Docker compose ([#4379](https://github.com/cookiecutter/cookiecutter-django/pull/4379))

- Update to Python 3.11.4 in local Docker compose ([#4380](https://github.com/cookiecutter/cookiecutter-django/pull/4380))

- Update celery to 5.3.0 ([#4369](https://github.com/cookiecutter/cookiecutter-django/pull/4369))

- Update werkzeug to 2.3.5 ([#4377](https://github.com/cookiecutter/cookiecutter-django/pull/4377))

## 2023.06.07


### Changed

- Replace `runserver` with `runserver_plus` ([#4373](https://github.com/cookiecutter/cookiecutter-django/pull/4373))

- Add translations for Brazilian Portuguese ([#4367](https://github.com/cookiecutter/cookiecutter-django/pull/4367))

### Updated

- Update sentry-sdk to 1.25.1 ([#4376](https://github.com/cookiecutter/cookiecutter-django/pull/4376))

- Update django-extensions to 3.2.3 ([#4372](https://github.com/cookiecutter/cookiecutter-django/pull/4372))

- Update djangorestframework-stubs to 3.14.1 ([#4366](https://github.com/cookiecutter/cookiecutter-django/pull/4366))

- Update django-stubs to 4.2.1 ([#4365](https://github.com/cookiecutter/cookiecutter-django/pull/4365))

- Update mypy to 1.3.0 ([#4327](https://github.com/cookiecutter/cookiecutter-django/pull/4327))

## 2023.06.02


### Updated

- Update sentry-sdk to 1.25.0 ([#4364](https://github.com/cookiecutter/cookiecutter-django/pull/4364))

## 2023.05.30


### Updated

- Update hiredis to 2.2.3 ([#4360](https://github.com/cookiecutter/cookiecutter-django/pull/4360))

- Update django-debug-toolbar to 4.1.0 ([#4359](https://github.com/cookiecutter/cookiecutter-django/pull/4359))

- Update redis to 4.5.5 ([#4358](https://github.com/cookiecutter/cookiecutter-django/pull/4358))

- Update django-anymail to 10.0 ([#4357](https://github.com/cookiecutter/cookiecutter-django/pull/4357))

- Update coverage to 7.2.7 ([#4356](https://github.com/cookiecutter/cookiecutter-django/pull/4356))

## 2023.05.28


## 2023.05.24


### Fixed

- Prevent Celery restarts on media file changes ([#4352](https://github.com/cookiecutter/cookiecutter-django/pull/4352))

### Updated

- Update coverage to 7.2.6 ([#4351](https://github.com/cookiecutter/cookiecutter-django/pull/4351))

## 2023.05.23


### Changed

- Fix compatibility webpack-bundle-tracker&gt;=2.0.0 js library required after upgrade django-webpack-loader&gt;=2.0.0 ([#4350](https://github.com/cookiecutter/cookiecutter-django/pull/4350))

### Updated

- Update sphinx-rtd-theme to 1.2.1 ([#4348](https://github.com/cookiecutter/cookiecutter-django/pull/4348))

- Update sentry-sdk to 1.24.0 ([#4349](https://github.com/cookiecutter/cookiecutter-django/pull/4349))

- Bump webpack-bundle-tracker from 1.8.1 to 2.0.0 in /{{cookiecutter.project_slug}} ([#4347](https://github.com/cookiecutter/cookiecutter-django/pull/4347))

- Update django-webpack-loader to 2.0.0 ([#4345](https://github.com/cookiecutter/cookiecutter-django/pull/4345))

- Update pytest-xdist to 3.3.1 ([#4344](https://github.com/cookiecutter/cookiecutter-django/pull/4344))

- Update requests to 2.31.0 ([#4346](https://github.com/cookiecutter/cookiecutter-django/pull/4346))

## 2023.05.18


### Updated

- Update pre-commit to 3.3.2 ([#4342](https://github.com/cookiecutter/cookiecutter-django/pull/4342))

## 2023.05.17


### Updated

- Update sentry-sdk to 1.23.1 ([#4341](https://github.com/cookiecutter/cookiecutter-django/pull/4341))

## 2023.05.15


### Updated

- Update django-cors-headers to 4.0.0 ([#4329](https://github.com/cookiecutter/cookiecutter-django/pull/4329))

- Update sentry-sdk to 1.23.0 ([#4337](https://github.com/cookiecutter/cookiecutter-django/pull/4337))

## 2023.05.09


### Updated

- Update werkzeug to 2.3.4 ([#4325](https://github.com/cookiecutter/cookiecutter-django/pull/4325))

## 2023.05.08


### Updated

- Auto-update pre-commit hooks ([#4320](https://github.com/cookiecutter/cookiecutter-django/pull/4320))

- Update sentry-sdk to 1.22.2 ([#4321](https://github.com/cookiecutter/cookiecutter-django/pull/4321))

## 2023.05.04


### Changed

- Remove pytz from dependencies ([#4309](https://github.com/cookiecutter/cookiecutter-django/pull/4309))

### Updated

- Update django-anymail to 9.2 ([#4316](https://github.com/cookiecutter/cookiecutter-django/pull/4316))

- Update pre-commit to 3.3.1 ([#4315](https://github.com/cookiecutter/cookiecutter-django/pull/4315))

- Update coverage to 7.2.5 ([#4314](https://github.com/cookiecutter/cookiecutter-django/pull/4314))

- Update django to 4.1.9 ([#4313](https://github.com/cookiecutter/cookiecutter-django/pull/4313))

- Update sentry-sdk to 1.21.1 ([#4312](https://github.com/cookiecutter/cookiecutter-django/pull/4312))

- Update requests to 2.30.0 ([#4311](https://github.com/cookiecutter/cookiecutter-django/pull/4311))

## 2023.05.02


### Updated

- Upgrade traefik to 2.10.1 ([#4304](https://github.com/cookiecutter/cookiecutter-django/pull/4304))

- Update uvicorn to 0.22.0 ([#4305](https://github.com/cookiecutter/cookiecutter-django/pull/4305))

- Update werkzeug to 2.3.3 ([#4307](https://github.com/cookiecutter/cookiecutter-django/pull/4307))

## 2023.04.28


### Changed

- Add django-upgrade to pre-commit hooks ([#4298](https://github.com/cookiecutter/cookiecutter-django/pull/4298))

## 2023.04.27


### Updated

- Update djangorestframework-stubs to 3.14.0 ([#4303](https://github.com/cookiecutter/cookiecutter-django/pull/4303))

- Update werkzeug to 2.3.1 ([#4302](https://github.com/cookiecutter/cookiecutter-django/pull/4302))

- Update django-stubs to 4.2.0 ([#4301](https://github.com/cookiecutter/cookiecutter-django/pull/4301))

## 2023.04.26


### Updated

- Upgrade cssnano to v6.0.0 ([#4233](https://github.com/cookiecutter/cookiecutter-django/pull/4233))

- Upgrade concurrently to 8.0.1 ([#4237](https://github.com/cookiecutter/cookiecutter-django/pull/4237))

- Upgrade to node v18 ([#4294](https://github.com/cookiecutter/cookiecutter-django/pull/4294))

- Update coverage to 7.2.3 ([#4297](https://github.com/cookiecutter/cookiecutter-django/pull/4297))

- Update mypy to 1.2.0 ([#4295](https://github.com/cookiecutter/cookiecutter-django/pull/4295))

- Update werkzeug to 2.3.0 ([#4296](https://github.com/cookiecutter/cookiecutter-django/pull/4296))

## 2023.04.25


### Updated

- Update sentry-sdk to 1.21.0 ([#4293](https://github.com/cookiecutter/cookiecutter-django/pull/4293))

- Update sphinx to 6.2.1 ([#4292](https://github.com/cookiecutter/cookiecutter-django/pull/4292))

- Bump traefik from 2.9.10 to 2.10.0 ([#4290](https://github.com/cookiecutter/cookiecutter-django/pull/4290))

- Auto-update pre-commit hooks ([#4288](https://github.com/cookiecutter/cookiecutter-django/pull/4288))

## 2023.04.24


### Updated

- Auto-update pre-commit hooks ([#4286](https://github.com/cookiecutter/cookiecutter-django/pull/4286))

- Update sphinx to 6.2.0 ([#4285](https://github.com/cookiecutter/cookiecutter-django/pull/4285))

## 2023.04.19


### Updated

- Update sentry-sdk to 1.20.0 ([#4282](https://github.com/cookiecutter/cookiecutter-django/pull/4282))

## 2023.04.18


### Documentation

- Document how to add 3rd party packages with Docker ([#4279](https://github.com/cookiecutter/cookiecutter-django/pull/4279))

## 2023.04.15


### Changed

- Add username_type option ([#3958](https://github.com/cookiecutter/cookiecutter-django/pull/3958))

- Fix inconsistent line length and move configs to pyproject.toml ([#4276](https://github.com/cookiecutter/cookiecutter-django/pull/4276))

- Relax rules for linting of pull requests on this template ([#4273](https://github.com/cookiecutter/cookiecutter-django/pull/4273))

- Add more pre-commit hooks ([#4266](https://github.com/cookiecutter/cookiecutter-django/pull/4266))

- Upgrade Python to version 3.11 (Faster CPython) ([#4256](https://github.com/cookiecutter/cookiecutter-django/pull/4256))

### Updated

- Update drf-spectacular to 0.26.2 ([#4277](https://github.com/cookiecutter/cookiecutter-django/pull/4277))

- Update pytest to 7.3.1 ([#4272](https://github.com/cookiecutter/cookiecutter-django/pull/4272))

## 2023.04.13

### Updated
- Update tox to 4.4.12 ([#4271](https://github.com/cookiecutter/cookiecutter-django/pull/4271))

## 2023.04.10

### Updated
- Update pytest-sugar to 0.9.7 ([#4269](https://github.com/cookiecutter/cookiecutter-django/pull/4269))
- Update pytest to 7.3.0 ([#4268](https://github.com/cookiecutter/cookiecutter-django/pull/4268))

## 2023.04.07

### Updated
- Upgrade traefik to 2.9.10 ([#4267](https://github.com/cookiecutter/cookiecutter-django/pull/4267))

## 2023.04.05

### Changed
- Update indent for nginx config file ([#4260](https://github.com/cookiecutter/cookiecutter-django/pull/4260))
### Updated
- Update tox to 4.4.11 ([#4262](https://github.com/cookiecutter/cookiecutter-django/pull/4262))
- Update django to 4.1.8 ([#4258](https://github.com/cookiecutter/cookiecutter-django/pull/4258))
- Update pre-commit to 3.2.2 ([#4259](https://github.com/cookiecutter/cookiecutter-django/pull/4259))

## 2023.04.04

### Changed
- Upgrade to Django 4.1 ([#4028](https://github.com/cookiecutter/cookiecutter-django/pull/4028))
- Remove deprecated security setting ([#4247](https://github.com/cookiecutter/cookiecutter-django/pull/4247))
### Fixed
- Replace `runserver_plus` with `runserver` ([#4255](https://github.com/cookiecutter/cookiecutter-django/pull/4255))
- Fix traefik rule priority for media router ([#4244](https://github.com/cookiecutter/cookiecutter-django/pull/4244))
### Updated
- Update sentry-sdk to 1.19.0 ([#4254](https://github.com/cookiecutter/cookiecutter-django/pull/4254))
- Update django-debug-toolbar to 4.0.0 ([#4251](https://github.com/cookiecutter/cookiecutter-django/pull/4251))

## 2023.04.03

### Changed
- fix: Syntax for ignoring specific noqa errors ([#4250](https://github.com/cookiecutter/cookiecutter-django/pull/4250))
### Updated
- Update psycopg2-binary to 2.9.6 ([#4249](https://github.com/cookiecutter/cookiecutter-django/pull/4249))
- Update psycopg2 to 2.9.6 ([#4248](https://github.com/cookiecutter/cookiecutter-django/pull/4248))

## 2023.04.01

### Updated
- Update pytest-instafail to 0.5.0 ([#4240](https://github.com/cookiecutter/cookiecutter-django/pull/4240))
- Update pillow to 9.5.0 ([#4242](https://github.com/cookiecutter/cookiecutter-django/pull/4242))
- Update django-allauth to 0.54.0 ([#4241](https://github.com/cookiecutter/cookiecutter-django/pull/4241))

## 2023.03.29

### Updated
- Update redis to 4.5.4 ([#4239](https://github.com/cookiecutter/cookiecutter-django/pull/4239))
- Update pytz to 2023.3 ([#4238](https://github.com/cookiecutter/cookiecutter-django/pull/4238))
- Update black to 23.3.0 ([#4236](https://github.com/cookiecutter/cookiecutter-django/pull/4236))

## 2023.03.27

### Updated
- Update watchfiles to 0.19.0 ([#4232](https://github.com/cookiecutter/cookiecutter-django/pull/4232))

## 2023.03.26

### Updated
- Update pre-commit to 3.2.1 ([#4229](https://github.com/cookiecutter/cookiecutter-django/pull/4229))

## 2023.03.25

### Updated
- Update pytz to 2023.2 ([#4228](https://github.com/cookiecutter/cookiecutter-django/pull/4228))

## 2023.03.23

### Updated
- Bump traefik from 2.9.8 to 2.9.9 ([#4225](https://github.com/cookiecutter/cookiecutter-django/pull/4225))

## 2023.03.22

### Updated
- Update redis to 4.5.3 ([#4227](https://github.com/cookiecutter/cookiecutter-django/pull/4227))

## 2023.03.20

### Updated
- Update django-allauth to 0.53.1 ([#4223](https://github.com/cookiecutter/cookiecutter-django/pull/4223))
- Update redis to 4.5.2 ([#4222](https://github.com/cookiecutter/cookiecutter-django/pull/4222))

## 2023.03.18

### Updated
- Update drf-spectacular to 0.26.1 ([#4221](https://github.com/cookiecutter/cookiecutter-django/pull/4221))
- Update pygithub to 1.58.1 ([#4220](https://github.com/cookiecutter/cookiecutter-django/pull/4220))
- Update pre-commit to 3.2.0 ([#4219](https://github.com/cookiecutter/cookiecutter-django/pull/4219))

## 2023.03.16

### Changed
- Pin base Python Docker images to bugfix ([#4194](https://github.com/cookiecutter/cookiecutter-django/pull/4194))
### Fixed
- Trim leading and trailing space in `domain_name` and `email` ([#4163](https://github.com/cookiecutter/cookiecutter-django/pull/4163))
### Updated
- Update djangorestframework-stubs to 1.10.0 ([#4217](https://github.com/cookiecutter/cookiecutter-django/pull/4217))
- Update django-stubs to 1.16.0 ([#4216](https://github.com/cookiecutter/cookiecutter-django/pull/4216))
- Update coverage to 7.2.2 ([#4218](https://github.com/cookiecutter/cookiecutter-django/pull/4218))
- Update sentry-sdk to 1.17.0 ([#4215](https://github.com/cookiecutter/cookiecutter-django/pull/4215))
- Bump Docker python image from 3.10.9 to 3.10.10 on production Django ([#4214](https://github.com/cookiecutter/cookiecutter-django/pull/4214))
- Bump Docker python image from 3.10.9-slim-bullseye to 3.10.10-slim-bullseye for docs ([#4213](https://github.com/cookiecutter/cookiecutter-django/pull/4213))
- Bump Docker python image from 3.10.9-slim-bullseye to 3.10.10-slim-bullseye for local Django service ([#4212](https://github.com/cookiecutter/cookiecutter-django/pull/4212))
- Update uvicorn to 0.21.1 ([#4211](https://github.com/cookiecutter/cookiecutter-django/pull/4211))
- Update django-allauth to 0.53.0 ([#4210](https://github.com/cookiecutter/cookiecutter-django/pull/4210))

## 2023.03.14

### Updated
- Update django-celery-beat to 2.5.0 ([#4208](https://github.com/cookiecutter/cookiecutter-django/pull/4208))

## 2023.03.13

### Updated
- Update uvicorn to 0.21.0 ([#4203](https://github.com/cookiecutter/cookiecutter-django/pull/4203))
- Update django-anymail to 9.1 ([#4206](https://github.com/cookiecutter/cookiecutter-django/pull/4206))
- Update tox to 4.4.7 ([#4207](https://github.com/cookiecutter/cookiecutter-django/pull/4207))

## 2023.03.09

### Fixed
- Fix the omit configuration for coverage ([#4201](https://github.com/cookiecutter/cookiecutter-django/pull/4201))
### Updated
- Update ipdb to 0.13.13 ([#4202](https://github.com/cookiecutter/cookiecutter-django/pull/4202))

## 2023.03.07

### Updated
- Update mypy to 1.1.1 ([#4196](https://github.com/cookiecutter/cookiecutter-django/pull/4196))
- Update django-environ to 0.10.0 ([#4195](https://github.com/cookiecutter/cookiecutter-django/pull/4195))

## 2023.03.04

### Changed
- Add option to serve media files locally using nginx ([#2457](https://github.com/cookiecutter/cookiecutter-django/pull/2457))
### Documentation
- Include contributing page to the docs ([#4144](https://github.com/cookiecutter/cookiecutter-django/pull/4144))
### Updated
- Update myst-parser to 0.19.1 ([#4193](https://github.com/cookiecutter/cookiecutter-django/pull/4193))
- Update pytest to 7.2.2 ([#4191](https://github.com/cookiecutter/cookiecutter-django/pull/4191))
- Update drf-spectacular to 0.26.0 ([#4192](https://github.com/cookiecutter/cookiecutter-django/pull/4192))

## 2023.02.28

### Updated
- Update pre-commit to 3.1.1 ([#4188](https://github.com/cookiecutter/cookiecutter-django/pull/4188))

## 2023.02.27

### Updated
- Update sentry-sdk to 1.16.0 ([#4187](https://github.com/cookiecutter/cookiecutter-django/pull/4187))

## 2023.02.26

### Changed
- Fix readthedocs config file for generated project ([#4172](https://github.com/cookiecutter/cookiecutter-django/pull/4172))
### Updated
- Bump traefik from v2.2.11 to 2.9.8 ([#4164](https://github.com/cookiecutter/cookiecutter-django/pull/4164))
- Update coverage to 7.2.1 ([#4186](https://github.com/cookiecutter/cookiecutter-django/pull/4186))

## 2023.02.25

### Changed
- Run linting with pre-commit on GitLab ([#4150](https://github.com/cookiecutter/cookiecutter-django/pull/4150))
### Fixed
- Disable caching for linter job on GitHub actions ([#4166](https://github.com/cookiecutter/cookiecutter-django/pull/4166))
### Documentation
- Add instuction to run celery beat ([#4162](https://github.com/cookiecutter/cookiecutter-django/pull/4162))
### Updated
- Bump garland/aws-cli-docker from 1.15.47 to 1.16.140 ([#4136](https://github.com/cookiecutter/cookiecutter-django/pull/4136))
- Update djangorestframework-stubs to 1.9.1 ([#4184](https://github.com/cookiecutter/cookiecutter-django/pull/4184))
- Update whitenoise to 6.4.0 ([#4180](https://github.com/cookiecutter/cookiecutter-django/pull/4180))
- Update django-stubs to 1.15.0 ([#4183](https://github.com/cookiecutter/cookiecutter-django/pull/4183))
- Update django-crispy-forms to 2.0 ([#4158](https://github.com/cookiecutter/cookiecutter-django/pull/4158))
- Update django-cors-headers to 3.14.0 ([#4181](https://github.com/cookiecutter/cookiecutter-django/pull/4181))
- Update python-slugify to 8.0.1 ([#4178](https://github.com/cookiecutter/cookiecutter-django/pull/4178))
- Update pre-commit to 3.1.0 ([#4176](https://github.com/cookiecutter/cookiecutter-django/pull/4176))
- Update mypy to 1.0.1 ([#4168](https://github.com/cookiecutter/cookiecutter-django/pull/4168))
- Update werkzeug to 2.2.3 ([#4160](https://github.com/cookiecutter/cookiecutter-django/pull/4160))
- Update coverage to 7.2.0 ([#4177](https://github.com/cookiecutter/cookiecutter-django/pull/4177))
- Update django to 4.0.10 ([#4159](https://github.com/cookiecutter/cookiecutter-django/pull/4159))
- Update hiredis to 2.2.2 ([#4156](https://github.com/cookiecutter/cookiecutter-django/pull/4156))

## 2023.02.17

### Changed
- Update version of github actions on the template project ([#4167](https://github.com/cookiecutter/cookiecutter-django/pull/4167))

## 2023.02.09

### Changed
- Remove unused pip cache paths in GHA &amp; add a note for pre-commit.ci ([#4151](https://github.com/cookiecutter/cookiecutter-django/pull/4151))
### Updated
- Update mypy to 0.991 ([#4106](https://github.com/cookiecutter/cookiecutter-django/pull/4106))

## 2023.02.08

### Updated
- Update sphinx to 6.1.3 ([#4148](https://github.com/cookiecutter/cookiecutter-django/pull/4148))
- Update redis to 4.5.1 ([#4147](https://github.com/cookiecutter/cookiecutter-django/pull/4147))

## 2023.02.07

### Updated
- Bump postcss-preset-env from 7.8.3 to 8.0.1 ([#4115](https://github.com/cookiecutter/cookiecutter-django/pull/4115))
- Bump sass-loader from 12.6.0 to 13.2.0 ([#4116](https://github.com/cookiecutter/cookiecutter-django/pull/4116))
- Bump babel-loader from 8.3.0 to 9.1.2 ([#4117](https://github.com/cookiecutter/cookiecutter-django/pull/4117))
- Bump postcss-loader from 6.2.1 to 7.0.2 ([#4114](https://github.com/cookiecutter/cookiecutter-django/pull/4114))
- Bump webpack-cli from 4.10.0 to 5.0.1 ([#4118](https://github.com/cookiecutter/cookiecutter-django/pull/4118))
- Update redis to 4.5.0 ([#4142](https://github.com/cookiecutter/cookiecutter-django/pull/4142))
- Update sentry-sdk to 1.15.0 ([#4141](https://github.com/cookiecutter/cookiecutter-django/pull/4141))

## 2023.02.06

### Changed
- Change `RequestFactory` to `APIRequestFactory` in tests for API views ([#4110](https://github.com/cookiecutter/cookiecutter-django/pull/4110))
### Fixed
- Fix django-webpack-loader setup when running tests ([#4128](https://github.com/cookiecutter/cookiecutter-django/pull/4128))
### Documentation
- Added AWS ECS Full Deployment Article to README ([#2630](https://github.com/cookiecutter/cookiecutter-django/pull/2630))
### Updated
- Update hiredis to 2.2.1 ([#4123](https://github.com/cookiecutter/cookiecutter-django/pull/4123))
- Update tox to 4.4.4 ([#4133](https://github.com/cookiecutter/cookiecutter-django/pull/4133))
- Update django to 4.0.9 ([#4134](https://github.com/cookiecutter/cookiecutter-django/pull/4134))
- Update django-webpack-loader to 1.8.1 ([#4132](https://github.com/cookiecutter/cookiecutter-django/pull/4132))

## 2023.02.05

### Documentation
- Add note about which service to request when running locally with Docker &amp; Webpack or Gulp ([#4130](https://github.com/cookiecutter/cookiecutter-django/pull/4130))

## 2023.02.03

### Updated
- Update pre-commit to 3.0.4 ([#4127](https://github.com/cookiecutter/cookiecutter-django/pull/4127))

## 2023.02.02

### Updated
- Update python-slugify to 8.0.0 ([#4111](https://github.com/cookiecutter/cookiecutter-django/pull/4111))
- Update pre-commit to 3.0.3 ([#4121](https://github.com/cookiecutter/cookiecutter-django/pull/4121))
- Update black to 23.1.0 ([#4120](https://github.com/cookiecutter/cookiecutter-django/pull/4120))
- Update black pre-commit hook ([#4122](https://github.com/cookiecutter/cookiecutter-django/pull/4122))

## 2023.01.29

### Changed
- Add Webpack support  ([#3623](https://github.com/cookiecutter/cookiecutter-django/pull/3623))
- Remove `BrokenLinkEmailsMiddleware` ([#4112](https://github.com/cookiecutter/cookiecutter-django/pull/4112))

## 2023.01.28

### Changed
- Refactor `merge_production_dotenvs_in_dotenv.py` ([#4105](https://github.com/cookiecutter/cookiecutter-django/pull/4105))
### Updated
- Update isort to 5.12.0 ([#4109](https://github.com/cookiecutter/cookiecutter-django/pull/4109))
- Auto-update pre-commit hooks ([#4108](https://github.com/cookiecutter/cookiecutter-django/pull/4108))

## 2023.01.27

### Updated
- Update django-stubs to 1.14.0 ([#4103](https://github.com/cookiecutter/cookiecutter-django/pull/4103))

## 2023.01.26

### Changed
- Rename BASE_DIR_PATH to BASE_DIR ([#4102](https://github.com/cookiecutter/cookiecutter-django/pull/4102))
### Updated
- Update pre-commit to 3.0.1 ([#4104](https://github.com/cookiecutter/cookiecutter-django/pull/4104))
- Update tox to 4.4.2 ([#4101](https://github.com/cookiecutter/cookiecutter-django/pull/4101))

## 2023.01.25

### Changed
- Rename ROOT_DIR to BASE_DIR ([#4086](https://github.com/cookiecutter/cookiecutter-django/pull/4086))
- Update postgres and redis to point to mini tiers ([#4099](https://github.com/cookiecutter/cookiecutter-django/pull/4099))
### Updated
- Update coverage to 7.1.0 ([#4100](https://github.com/cookiecutter/cookiecutter-django/pull/4100))

## 2023.01.24

### Updated
- Update pre-commit to 3.0.0 ([#4098](https://github.com/cookiecutter/cookiecutter-django/pull/4098))

## 2023.01.23

### Updated
- Update sentry-sdk to 1.14.0 ([#4096](https://github.com/cookiecutter/cookiecutter-django/pull/4096))

## 2023.01.22

### Updated
- Update django-compressor to 4.3.1 ([#4094](https://github.com/cookiecutter/cookiecutter-django/pull/4094))

## 2023.01.21

### Updated
- Update django-stubs to 1.13.2 ([#4093](https://github.com/cookiecutter/cookiecutter-django/pull/4093))

## 2023.01.19

### Fixed
- Add sourcemaps support to Gulp ([#4089](https://github.com/cookiecutter/cookiecutter-django/pull/4089))
### Updated
- Update coverage to 7.0.5 ([#4092](https://github.com/cookiecutter/cookiecutter-django/pull/4092))
- Update redis to 4.4.2 ([#4091](https://github.com/cookiecutter/cookiecutter-django/pull/4091))
- Update requests to 2.28.2 ([#4090](https://github.com/cookiecutter/cookiecutter-django/pull/4090))
- Update tox to 4.3.5 ([#4087](https://github.com/cookiecutter/cookiecutter-django/pull/4087))

## 2023.01.17

### Updated
- Update tox to 4.3.3 ([#4081](https://github.com/cookiecutter/cookiecutter-django/pull/4081))

## 2023.01.15

### Updated
- Update pytest to 7.2.1 ([#4077](https://github.com/cookiecutter/cookiecutter-django/pull/4077))
- Update pytz to 2022.7.1 ([#4078](https://github.com/cookiecutter/cookiecutter-django/pull/4078))

## 2023.01.12

### Updated
- Update sentry-sdk to 1.13.0 ([#4074](https://github.com/cookiecutter/cookiecutter-django/pull/4074))

## 2023.01.11

### Changed
- Update Celery instructions in the documentation ([#4061](https://github.com/cookiecutter/cookiecutter-django/pull/4061))
### Updated
- Update tox to 4.2.7 ([#4073](https://github.com/cookiecutter/cookiecutter-django/pull/4073))

## 2023.01.10

### Changed
- Add dump.rdb to gitignore ([#4062](https://github.com/cookiecutter/cookiecutter-django/pull/4062))
### Fixed
- Exclude `.venv` from code style checks ([#4069](https://github.com/cookiecutter/cookiecutter-django/pull/4069))
### Updated
- Update hiredis to 2.1.1 ([#4070](https://github.com/cookiecutter/cookiecutter-django/pull/4070))

## 2023.01.08

### Updated
- Update redis to 4.4.1 ([#4068](https://github.com/cookiecutter/cookiecutter-django/pull/4068))
- Update coverage to 7.0.4 ([#4067](https://github.com/cookiecutter/cookiecutter-django/pull/4067))

## 2023.01.07

### Updated
- Update tox to 4.2.6 ([#4064](https://github.com/cookiecutter/cookiecutter-django/pull/4064))
- Update django-storages to 1.13.2 ([#4057](https://github.com/cookiecutter/cookiecutter-django/pull/4057))
- Update isort to 5.11.4 ([#4058](https://github.com/cookiecutter/cookiecutter-django/pull/4058))
- Update rcssmin to 1.1.1 ([#4060](https://github.com/cookiecutter/cookiecutter-django/pull/4060))
- Update django-compressor to 4.3 ([#4063](https://github.com/cookiecutter/cookiecutter-django/pull/4063))

## 2023.01.06

### Changed
- Add `.git` to `.dockerignore` ([#4054](https://github.com/cookiecutter/cookiecutter-django/pull/4054))
- Fix link and add non-Docker commands to testing page in the docs ([#4036](https://github.com/cookiecutter/cookiecutter-django/pull/4036))
### Updated
- Update tox to 4.2.3 ([#4051](https://github.com/cookiecutter/cookiecutter-django/pull/4051))

## 2023.01.04

### Changed
- Fix typo on test settings ([#4049](https://github.com/cookiecutter/cookiecutter-django/pull/4049))
### Updated
- Update tox to 4.2.2 ([#4050](https://github.com/cookiecutter/cookiecutter-django/pull/4050))
- Update tox to 4.2.1 ([#4046](https://github.com/cookiecutter/cookiecutter-django/pull/4046))
- Update coverage to 7.0.3 ([#4047](https://github.com/cookiecutter/cookiecutter-django/pull/4047))

## 2023.01.03

### Updated
- Update flake8-isort to 6.0.0 ([#4022](https://github.com/cookiecutter/cookiecutter-django/pull/4022))
- Update tox to 4.1.3 ([#4041](https://github.com/cookiecutter/cookiecutter-django/pull/4041))
- Update pillow to 9.4.0 ([#4040](https://github.com/cookiecutter/cookiecutter-django/pull/4040))
- Update gitpython to 3.1.30 ([#4032](https://github.com/cookiecutter/cookiecutter-django/pull/4032))
- Update coverage to 7.0.2 ([#4042](https://github.com/cookiecutter/cookiecutter-django/pull/4042))
- Update whitenoise to 6.3.0 ([#4044](https://github.com/cookiecutter/cookiecutter-django/pull/4044))

## 2022.12.29

### Updated
- Update tox to 4.1.0 ([#4035](https://github.com/cookiecutter/cookiecutter-django/pull/4035))
- Update tox to 4.0.19 ([#4030](https://github.com/cookiecutter/cookiecutter-django/pull/4030))
- Update django-allauth to 0.52.0 ([#4033](https://github.com/cookiecutter/cookiecutter-django/pull/4033))

## 2022.12.26

### Updated
- Update tox to 4.0.17 ([#4027](https://github.com/cookiecutter/cookiecutter-django/pull/4027))
- Update pre-commit to 2.21.0 ([#4026](https://github.com/cookiecutter/cookiecutter-django/pull/4026))

## 2022.12.25

### Updated
- Auto-update pre-commit hooks ([#4021](https://github.com/cookiecutter/cookiecutter-django/pull/4021))

## 2022.12.24

### Updated
- Update coverage to 7.0.1 ([#4024](https://github.com/cookiecutter/cookiecutter-django/pull/4024))

## 2022.12.21

### Changed
- Retry when trying to store a Celery result in backend ([#3996](https://github.com/cookiecutter/cookiecutter-django/pull/3996))
- Update image URL for build status shield badge ([#4018](https://github.com/cookiecutter/cookiecutter-django/pull/4018))
### Updated
- Update pytz to 2022.7 ([#4020](https://github.com/cookiecutter/cookiecutter-django/pull/4020))
- Update ipdb to 0.13.11 ([#4019](https://github.com/cookiecutter/cookiecutter-django/pull/4019))
- Update tox to 4.0.16 ([#4017](https://github.com/cookiecutter/cookiecutter-django/pull/4017))
- Update sentry-sdk to 1.12.1 ([#4014](https://github.com/cookiecutter/cookiecutter-django/pull/4014))
- Update coverage to 7.0.0 ([#4013](https://github.com/cookiecutter/cookiecutter-django/pull/4013))
- Update django-anymail to 9.0 ([#4012](https://github.com/cookiecutter/cookiecutter-django/pull/4012))
- Auto-update pre-commit hooks ([#4005](https://github.com/cookiecutter/cookiecutter-django/pull/4005))
- Update isort to 5.11.3 ([#4010](https://github.com/cookiecutter/cookiecutter-django/pull/4010))
- Update drf-spectacular to 0.25.1 ([#4009](https://github.com/cookiecutter/cookiecutter-django/pull/4009))
- Update hiredis to 2.1.0 ([#4006](https://github.com/cookiecutter/cookiecutter-django/pull/4006))

## 2022.12.13

### Changed
- Improve documentation for Getting started with Docker ([#4003](https://github.com/cookiecutter/cookiecutter-django/pull/4003))
### Updated
- Update isort to 5.11.1 ([#3999](https://github.com/cookiecutter/cookiecutter-django/pull/3999))
- Auto-update pre-commit hooks ([#3998](https://github.com/cookiecutter/cookiecutter-django/pull/3998))
- Update isort to 5.11.0 ([#3997](https://github.com/cookiecutter/cookiecutter-django/pull/3997))

## 2022.12.10

### Updated
- Update tox to 4.0.5 ([#3993](https://github.com/cookiecutter/cookiecutter-django/pull/3993))
- Auto-update pre-commit hooks ([#3991](https://github.com/cookiecutter/cookiecutter-django/pull/3991))

## 2022.12.09

### Changed
- Remove bind option mounts for docker compose volumes ([#3981](https://github.com/cookiecutter/cookiecutter-django/pull/3981))
### Updated
- Update djangorestframework-stubs to 1.8.0 ([#3990](https://github.com/cookiecutter/cookiecutter-django/pull/3990))
- Update black to 22.12.0 ([#3988](https://github.com/cookiecutter/cookiecutter-django/pull/3988))

## 2022.12.08

### Updated
- Update tox to 4.0.3 ([#3987](https://github.com/cookiecutter/cookiecutter-django/pull/3987))
- Update tox to 4.0.2 ([#3985](https://github.com/cookiecutter/cookiecutter-django/pull/3985))
- Update django-stubs to 1.13.1 ([#3986](https://github.com/cookiecutter/cookiecutter-django/pull/3986))

## 2022.12.07

### Updated
- Auto-update pre-commit hooks ([#3983](https://github.com/cookiecutter/cookiecutter-django/pull/3983))

## 2022.12.06

### Changed
- Simplify production `DATABASES` setting to extend base definition ([#3969](https://github.com/cookiecutter/cookiecutter-django/pull/3969))
### Fixed
- Only set `SERVERS` for `drf-spectacular` in production ([#3609](https://github.com/cookiecutter/cookiecutter-django/pull/3609))
### Updated
- Update django-coverage-plugin to 3.0.0 ([#3979](https://github.com/cookiecutter/cookiecutter-django/pull/3979))
- Bump stefanzweifel/git-auto-commit-action from 4.15.4 to 4.16.0 ([#3978](https://github.com/cookiecutter/cookiecutter-django/pull/3978))

## 2022.12.04

### Updated
- Update redis to 4.4.0 ([#3977](https://github.com/cookiecutter/cookiecutter-django/pull/3977))
- Update django-debug-toolbar to 3.8.1 ([#3976](https://github.com/cookiecutter/cookiecutter-django/pull/3976))

## 2022.12.03

### Updated
- Auto-update pre-commit hooks ([#3975](https://github.com/cookiecutter/cookiecutter-django/pull/3975))

## 2022.12.02

### Updated
- Update flake8 to 6.0.0 ([#3974](https://github.com/cookiecutter/cookiecutter-django/pull/3974))

## 2022.11.30

### Changed
- Add Azure Storage as an option to serve static and media files ([#3967](https://github.com/cookiecutter/cookiecutter-django/pull/3967))
### Updated
- Auto-update pre-commit hooks ([#3970](https://github.com/cookiecutter/cookiecutter-django/pull/3970))

## 2022.11.26

### Changed
- Fix typo in flower start for watching celery ([#3966](https://github.com/cookiecutter/cookiecutter-django/pull/3966))

## 2022.11.24

### Updated
- Auto-update pre-commit hooks ([#3963](https://github.com/cookiecutter/cookiecutter-django/pull/3963))

## 2022.11.23

### Changed
- Fix graceful shutdown of local dev containers and use watchfiles for beat + flower ([#3925](https://github.com/cookiecutter/cookiecutter-django/pull/3925))
- feat(celery): Enable sending the sent task event by default ([#3961](https://github.com/cookiecutter/cookiecutter-django/pull/3961))
### Updated
- Bump stefanzweifel/git-auto-commit-action from 4.15.3 to 4.15.4 ([#3940](https://github.com/cookiecutter/cookiecutter-django/pull/3940))
- Update django-model-utils to 4.3.1 ([#3948](https://github.com/cookiecutter/cookiecutter-django/pull/3948))
- Update flake8-isort to 5.0.3 ([#3952](https://github.com/cookiecutter/cookiecutter-django/pull/3952))

## 2022.11.22

### Changed
- Remove USE_L10N due to deprecation ([#3960](https://github.com/cookiecutter/cookiecutter-django/pull/3960))
- Remove platform from compose file ([#3957](https://github.com/cookiecutter/cookiecutter-django/pull/3957))
- feat(celery): Send task events for Celery by default ([#3959](https://github.com/cookiecutter/cookiecutter-django/pull/3959))
### Updated
- Update python-slugify to 7.0.0 ([#3950](https://github.com/cookiecutter/cookiecutter-django/pull/3950))
- Update redis to 4.3.5 ([#3954](https://github.com/cookiecutter/cookiecutter-django/pull/3954))
- Update sentry-sdk to 1.11.1 ([#3955](https://github.com/cookiecutter/cookiecutter-django/pull/3955))
- Update uvicorn to 0.20.0 ([#3953](https://github.com/cookiecutter/cookiecutter-django/pull/3953))
- Update tox to 3.27.1 ([#3945](https://github.com/cookiecutter/cookiecutter-django/pull/3945))

## 2022.11.11

### Updated
- Auto-update pre-commit hooks ([#3942](https://github.com/cookiecutter/cookiecutter-django/pull/3942))

## 2022.11.07

### Updated
- Update watchfiles to 0.18.1 ([#3938](https://github.com/cookiecutter/cookiecutter-django/pull/3938))

## 2022.11.06

### Changed
- Store extended Celery task attributes in backend ([#3855](https://github.com/cookiecutter/cookiecutter-django/pull/3855))
- add os requirements for Ubuntu 22.04 (Jammy) ([#3930](https://github.com/cookiecutter/cookiecutter-django/pull/3930))
### Updated
- Update pytest-sugar to 0.9.6 ([#3937](https://github.com/cookiecutter/cookiecutter-django/pull/3937))
- Update pygithub to 1.57 ([#3936](https://github.com/cookiecutter/cookiecutter-django/pull/3936))
- Update sphinx-rtd-theme to 1.1.1 ([#3935](https://github.com/cookiecutter/cookiecutter-django/pull/3935))

## 2022.11.02

### Changed
- fix typo in CONTRIBUTING.md ([#3932](https://github.com/cookiecutter/cookiecutter-django/pull/3932))
### Updated
- Update crispy-bootstrap5 to 0.7 ([#3886](https://github.com/cookiecutter/cookiecutter-django/pull/3886))
- Update django-coverage-plugin to 2.0.4 ([#3927](https://github.com/cookiecutter/cookiecutter-django/pull/3927))
- Update pytz to 2022.6 ([#3928](https://github.com/cookiecutter/cookiecutter-django/pull/3928))
- Update sphinx-rtd-theme to 1.1.0 ([#3929](https://github.com/cookiecutter/cookiecutter-django/pull/3929))
- Update pillow to 9.3.0 ([#3922](https://github.com/cookiecutter/cookiecutter-django/pull/3922))

## 2022.10.30

### Updated
- Auto-update pre-commit hooks ([#3924](https://github.com/cookiecutter/cookiecutter-django/pull/3924))

## 2022.10.28

### Updated
- Bump stefanzweifel/git-auto-commit-action from 4.15.2 to 4.15.3 ([#3921](https://github.com/cookiecutter/cookiecutter-django/pull/3921))

## 2022.10.26

### Updated
- Update uvicorn to 0.19.0 ([#3920](https://github.com/cookiecutter/cookiecutter-django/pull/3920))
- Update pytest to 7.2.0 ([#3919](https://github.com/cookiecutter/cookiecutter-django/pull/3919))
- Update tox to 3.27.0 ([#3917](https://github.com/cookiecutter/cookiecutter-django/pull/3917))
- Update psycopg2 to 2.9.5 ([#3918](https://github.com/cookiecutter/cookiecutter-django/pull/3918))

## 2022.10.24

### Changed
- Upgrade Python version from 3.9 to 3.10 ([#3913](https://github.com/cookiecutter/cookiecutter-django/pull/3913))
### Updated
- Update sentry-sdk to 1.10.1 ([#3911](https://github.com/cookiecutter/cookiecutter-django/pull/3911))
- Bump stefanzweifel/git-auto-commit-action from 4.15.1 to 4.15.2 ([#3914](https://github.com/cookiecutter/cookiecutter-django/pull/3914))

## 2022.10.19

### Changed
- Set AWS_S3_MAX_MEMORY_SIZE ([#3810](https://github.com/cookiecutter/cookiecutter-django/pull/3810))
- Upgrade to Django 4.0 ([#3848](https://github.com/cookiecutter/cookiecutter-django/pull/3848))
### Updated
- Update pytz to 2022.5 ([#3906](https://github.com/cookiecutter/cookiecutter-django/pull/3906))
- Update sphinx to 5.3.0 ([#3905](https://github.com/cookiecutter/cookiecutter-django/pull/3905))
- Update django-celery-beat to 2.4.0 ([#3908](https://github.com/cookiecutter/cookiecutter-django/pull/3908))
- Update watchfiles to 0.18.0 ([#3907](https://github.com/cookiecutter/cookiecutter-django/pull/3907))

## 2022.10.13

### Updated
- Update pygithub to 1.56 ([#3904](https://github.com/cookiecutter/cookiecutter-django/pull/3904))

## 2022.10.11

### Updated
- Auto-update pre-commit hooks ([#3899](https://github.com/cookiecutter/cookiecutter-django/pull/3899))
- Update flake8-isort to 5.0.0 ([#3901](https://github.com/cookiecutter/cookiecutter-django/pull/3901))
- Update gitpython to 3.1.29 ([#3902](https://github.com/cookiecutter/cookiecutter-django/pull/3902))
- Update psycopg2 to 2.9.4 ([#3896](https://github.com/cookiecutter/cookiecutter-django/pull/3896))
- Bump stefanzweifel/git-auto-commit-action from 4.15.0 to 4.15.1 ([#3903](https://github.com/cookiecutter/cookiecutter-django/pull/3903))
- Update black to 22.10.0 ([#3898](https://github.com/cookiecutter/cookiecutter-django/pull/3898))

## 2022.10.04

### Updated
- Update django to 3.2.16 ([#3895](https://github.com/cookiecutter/cookiecutter-django/pull/3895))
- Update mypy to 0.982 ([#3893](https://github.com/cookiecutter/cookiecutter-django/pull/3893))
- Auto-update pre-commit hooks ([#3894](https://github.com/cookiecutter/cookiecutter-django/pull/3894))

## 2022.10.03

### Updated
- Update sentry-sdk to 1.9.10 ([#3892](https://github.com/cookiecutter/cookiecutter-django/pull/3892))

## 2022.10.02

### Updated
- Update pytz to 2022.4 ([#3891](https://github.com/cookiecutter/cookiecutter-django/pull/3891))

## 2022.09.30

### Updated
- Update coverage to 6.5.0 ([#3890](https://github.com/cookiecutter/cookiecutter-django/pull/3890))
- Update mypy to 0.981 ([#3889](https://github.com/cookiecutter/cookiecutter-django/pull/3889))
- Update sentry-sdk to 1.9.9 ([#3888](https://github.com/cookiecutter/cookiecutter-django/pull/3888))
- Update sphinx to 5.2.3 ([#3887](https://github.com/cookiecutter/cookiecutter-django/pull/3887))

## 2022.09.29

### Changed
- Remove outdated &amp; optional Sendgrid settings from production config ([#3885](https://github.com/cookiecutter/cookiecutter-django/pull/3885))

## 2022.09.27

### Updated
- Update sphinx to 5.2.2 ([#3884](https://github.com/cookiecutter/cookiecutter-django/pull/3884))

## 2022.09.26

### Updated
- Update drf-spectacular to 0.24.2 ([#3882](https://github.com/cookiecutter/cookiecutter-django/pull/3882))
- Update djangorestframework to 3.14.0 ([#3881](https://github.com/cookiecutter/cookiecutter-django/pull/3881))
- Update django-debug-toolbar to 3.7.0 ([#3878](https://github.com/cookiecutter/cookiecutter-django/pull/3878))
- Auto-update pre-commit hooks ([#3877](https://github.com/cookiecutter/cookiecutter-django/pull/3877))
- Bump stefanzweifel/git-auto-commit-action from 4.14.1 to 4.15.0 ([#3880](https://github.com/cookiecutter/cookiecutter-django/pull/3880))
- Update sphinx to 5.2.1 ([#3879](https://github.com/cookiecutter/cookiecutter-django/pull/3879))

## 2022.09.24

### Fixed
- Remove `--no-deps` in pip wheels command of docs Dockerfile ([#3875](https://github.com/cookiecutter/cookiecutter-django/pull/3875))

## 2022.09.23

### Changed
- Reload uvicorn on html file change ([#3866](https://github.com/cookiecutter/cookiecutter-django/pull/3866))
- Mailjet default api url does not work out of the box ([#3871](https://github.com/cookiecutter/cookiecutter-django/pull/3871))
### Updated
- Auto-update pre-commit hooks ([#3872](https://github.com/cookiecutter/cookiecutter-django/pull/3872))
- Update django-extensions to 3.2.1 ([#3867](https://github.com/cookiecutter/cookiecutter-django/pull/3867))
- Update tox to 3.26.0 ([#3864](https://github.com/cookiecutter/cookiecutter-django/pull/3864))
- Update drf-spectacular to 0.24.1 ([#3874](https://github.com/cookiecutter/cookiecutter-django/pull/3874))

## 2022.09.15

### Updated
- Update watchfiles to 0.17.0 ([#3869](https://github.com/cookiecutter/cookiecutter-django/pull/3869))
- Update drf-spectacular to 0.24.0 ([#3870](https://github.com/cookiecutter/cookiecutter-django/pull/3870))

## 2022.09.05

### Updated
- Update sentry-sdk to 1.9.8 ([#3861](https://github.com/cookiecutter/cookiecutter-django/pull/3861))

## 2022.09.02

### Updated
- Update pytest to 7.1.3 ([#3860](https://github.com/cookiecutter/cookiecutter-django/pull/3860))
- Update sentry-sdk to 1.9.7 ([#3859](https://github.com/cookiecutter/cookiecutter-django/pull/3859))

## 2022.09.01

### Changed
- Add article to README about how to use a hosted DB ([#3844](https://github.com/cookiecutter/cookiecutter-django/pull/3844))
### Updated
- Update sentry-sdk to 1.9.6 ([#3856](https://github.com/cookiecutter/cookiecutter-django/pull/3856))
- Auto-update pre-commit hooks ([#3858](https://github.com/cookiecutter/cookiecutter-django/pull/3858))
- Update black to 22.8.0 ([#3857](https://github.com/cookiecutter/cookiecutter-django/pull/3857))

## 2022.08.26

### Changed
- Fix formatting in docs ([#3850](https://github.com/cookiecutter/cookiecutter-django/pull/3850))

## 2022.08.24

### Updated
- Update django-debug-toolbar to 3.6.0 ([#3847](https://github.com/cookiecutter/cookiecutter-django/pull/3847))
- Update werkzeug to 2.2.2 ([#3846](https://github.com/cookiecutter/cookiecutter-django/pull/3846))
- Update coverage to 6.4.4 ([#3842](https://github.com/cookiecutter/cookiecutter-django/pull/3842))
- Update uvicorn to 0.18.3 ([#3845](https://github.com/cookiecutter/cookiecutter-django/pull/3845))
- Update sentry-sdk to 1.9.5 ([#3841](https://github.com/cookiecutter/cookiecutter-django/pull/3841))
- Update flower to 1.2.0 ([#3836](https://github.com/cookiecutter/cookiecutter-django/pull/3836))
- Update django-storages to 1.13.1 ([#3833](https://github.com/cookiecutter/cookiecutter-django/pull/3833))

## 2022.08.15

### Updated
- Update coverage to 6.4.3 ([#3835](https://github.com/cookiecutter/cookiecutter-django/pull/3835))
- Update pytz to 2022.2.1 ([#3840](https://github.com/cookiecutter/cookiecutter-django/pull/3840))
- Update sentry-sdk to 1.9.4 ([#3838](https://github.com/cookiecutter/cookiecutter-django/pull/3838))

## 2022.08.09

### Updated
- Update sentry-sdk to 1.9.3 ([#3837](https://github.com/cookiecutter/cookiecutter-django/pull/3837))

## 2022.08.05

### Updated
- Update sentry-sdk to 1.9.2 ([#3832](https://github.com/cookiecutter/cookiecutter-django/pull/3832))

## 2022.08.04

### Updated
- Auto-update pre-commit hooks ([#3816](https://github.com/cookiecutter/cookiecutter-django/pull/3816))
- Update flake8 to 5.0.4 ([#3829](https://github.com/cookiecutter/cookiecutter-django/pull/3829))
- Update django-compressor to 4.1 ([#3823](https://github.com/cookiecutter/cookiecutter-django/pull/3823))
- Update flake8-isort to 4.2.0 ([#3828](https://github.com/cookiecutter/cookiecutter-django/pull/3828))

## 2022.08.03

### Updated
- Update django to 3.2.15 ([#3822](https://github.com/cookiecutter/cookiecutter-django/pull/3822))

## 2022.07.29

### Updated
- Update sentry-sdk to 1.9.0 ([#3815](https://github.com/cookiecutter/cookiecutter-django/pull/3815))

## 2022.07.28

### Updated
- Update werkzeug to 2.2.1 ([#3814](https://github.com/cookiecutter/cookiecutter-django/pull/3814))

## 2022.07.27

### Updated
- Update werkzeug to 2.2.0 ([#3813](https://github.com/cookiecutter/cookiecutter-django/pull/3813))
- Update sphinx to 5.1.1 ([#3811](https://github.com/cookiecutter/cookiecutter-django/pull/3811))
- Update drf-spectacular to 0.23.1 ([#3812](https://github.com/cookiecutter/cookiecutter-django/pull/3812))

## 2022.07.26

### Changed
- Switch from `watchgod` to `watchfiles` ([#3791](https://github.com/cookiecutter/cookiecutter-django/pull/3791))
- Change Django settings file used by pylint ([#3806](https://github.com/cookiecutter/cookiecutter-django/pull/3806))
- Simplify database access in tests ([#3807](https://github.com/cookiecutter/cookiecutter-django/pull/3807))
- Provide more context when wating for PostgreSQL takes too long ([#3782](https://github.com/cookiecutter/cookiecutter-django/pull/3782))
### Updated
- Update django-compressor to 4.0 ([#3802](https://github.com/cookiecutter/cookiecutter-django/pull/3802))
- Update flake8-isort to 4.1.2.post0 ([#3809](https://github.com/cookiecutter/cookiecutter-django/pull/3809))
- Update sphinx to 5.1.0 ([#3808](https://github.com/cookiecutter/cookiecutter-django/pull/3808))
- Update sh to 1.14.3 ([#3798](https://github.com/cookiecutter/cookiecutter-django/pull/3798))
- Auto-update pre-commit hooks ([#3780](https://github.com/cookiecutter/cookiecutter-django/pull/3780))

## 2022.07.22

### Updated
- Update pytest-sugar to 0.9.5 ([#3800](https://github.com/cookiecutter/cookiecutter-django/pull/3800))
- Update sphinx to 5.0.2 ([#3801](https://github.com/cookiecutter/cookiecutter-django/pull/3801))
- Update pillow to 9.2.0 ([#3799](https://github.com/cookiecutter/cookiecutter-django/pull/3799))
- Update werkzeug to 2.1.2 ([#3797](https://github.com/cookiecutter/cookiecutter-django/pull/3797))

## 2022.07.21

### Changed
- Set user to form instance in update user view test ([#3776](https://github.com/cookiecutter/cookiecutter-django/pull/3776))
- Fix warning from django-coverage-plugin in tests ([#3790](https://github.com/cookiecutter/cookiecutter-django/pull/3790))
- Always use `const` instead of `var` in `gulpfile.js` ([#3786](https://github.com/cookiecutter/cookiecutter-django/pull/3786))
### Updated
- Update flower to 1.1.0 ([#3796](https://github.com/cookiecutter/cookiecutter-django/pull/3796))
- Update coverage to 6.4.2 ([#3783](https://github.com/cookiecutter/cookiecutter-django/pull/3783))
- Update mypy to 0.971 ([#3788](https://github.com/cookiecutter/cookiecutter-django/pull/3788))
- Update sentry-sdk to 1.8.0 ([#3792](https://github.com/cookiecutter/cookiecutter-django/pull/3792))
- Update pre-commit to 2.20.0 ([#3779](https://github.com/cookiecutter/cookiecutter-django/pull/3779))
- Update django-extensions to 3.2.0 ([#3774](https://github.com/cookiecutter/cookiecutter-django/pull/3774))
- Update tox to 3.25.1 ([#3767](https://github.com/cookiecutter/cookiecutter-django/pull/3767))
- Update uvicorn to 0.18.2 ([#3762](https://github.com/cookiecutter/cookiecutter-django/pull/3762))
- Update redis to 4.3.4 ([#3763](https://github.com/cookiecutter/cookiecutter-django/pull/3763))
- Update requests to 2.28.1 ([#3766](https://github.com/cookiecutter/cookiecutter-django/pull/3766))

## 2022.07.10

### Changed
- Revert auto-update pre-commit hooks ([#3778](https://github.com/cookiecutter/cookiecutter-django/pull/3778))
### Updated
- Auto-update pre-commit hooks ([#3775](https://github.com/cookiecutter/cookiecutter-django/pull/3775))

## 2022.07.06

### Updated
- Update django to 3.2.14 ([#3768](https://github.com/cookiecutter/cookiecutter-django/pull/3768))

## 2022.06.28

### Updated
- Auto-update pre-commit hooks ([#3765](https://github.com/cookiecutter/cookiecutter-django/pull/3765))
- Update black to 22.6.0 ([#3764](https://github.com/cookiecutter/cookiecutter-django/pull/3764))

## 2022.06.23

### Updated
- Update django-debug-toolbar to 3.5.0 ([#3760](https://github.com/cookiecutter/cookiecutter-django/pull/3760))

## 2022.06.22

### Updated
- Update django-stubs to 1.12.0 ([#3757](https://github.com/cookiecutter/cookiecutter-django/pull/3757))
- Update sentry-sdk to 1.6.0 ([#3756](https://github.com/cookiecutter/cookiecutter-django/pull/3756))
- Update djangorestframework-stubs to 1.7.0 ([#3754](https://github.com/cookiecutter/cookiecutter-django/pull/3754))

## 2022.06.15

### Updated
- Update django-environ to 0.9.0 ([#3751](https://github.com/cookiecutter/cookiecutter-django/pull/3751))

## 2022.06.13

### Updated
- Update cookiecutter to 2.1.1 ([#3727](https://github.com/cookiecutter/cookiecutter-django/pull/3727))

## 2022.06.11

### Updated
- Update requests to 2.28.0 ([#3748](https://github.com/cookiecutter/cookiecutter-django/pull/3748))

## 2022.06.09

### Updated
- Bump actions/setup-python from 3 to 4 ([#3746](https://github.com/cookiecutter/cookiecutter-django/pull/3746))

## 2022.06.08

### Updated
- Auto-update pre-commit hooks ([#3744](https://github.com/cookiecutter/cookiecutter-django/pull/3744))

## 2022.06.07

### Updated
- Update django-allauth to 0.51.0 ([#3743](https://github.com/cookiecutter/cookiecutter-django/pull/3743))
- Auto-update pre-commit hooks ([#3742](https://github.com/cookiecutter/cookiecutter-django/pull/3742))

## 2022.06.06

### Updated
- Bump pre-commit/action from 2.0.3 to 3.0.0 ([#3739](https://github.com/cookiecutter/cookiecutter-django/pull/3739))

## 2022.06.05

### Updated
- Update whitenoise to 6.2.0 ([#3737](https://github.com/cookiecutter/cookiecutter-django/pull/3737))
- Update django-cors-headers to 3.13.0 ([#3738](https://github.com/cookiecutter/cookiecutter-django/pull/3738))

## 2022.06.04

### Updated
- Update django-cors-headers to 3.12.0 ([#3736](https://github.com/cookiecutter/cookiecutter-django/pull/3736))
- Update djangorestframework-stubs to 1.6.0 ([#3718](https://github.com/cookiecutter/cookiecutter-django/pull/3718))
- Update django-stubs to 1.11.0 ([#3734](https://github.com/cookiecutter/cookiecutter-django/pull/3734))
- Update sphinx to 5.0.1 ([#3733](https://github.com/cookiecutter/cookiecutter-django/pull/3733))
- Update sphinx to 5.0.0 ([#3724](https://github.com/cookiecutter/cookiecutter-django/pull/3724))
- Update celery to 5.2.7 ([#3732](https://github.com/cookiecutter/cookiecutter-django/pull/3732))
- Update django-celery-beat to 2.3.0 ([#3731](https://github.com/cookiecutter/cookiecutter-django/pull/3731))

## 2022.06.02

### Updated
- Update coverage to 6.4.1 ([#3729](https://github.com/cookiecutter/cookiecutter-django/pull/3729))
- Update redis to 4.3.3 ([#3728](https://github.com/cookiecutter/cookiecutter-django/pull/3728))

## 2022.06.01

### Updated
- Update redis to 4.3.2 ([#3726](https://github.com/cookiecutter/cookiecutter-django/pull/3726))

## 2022.05.24

### Updated
- Update coverage to 6.4 ([#3716](https://github.com/cookiecutter/cookiecutter-django/pull/3716))

## 2022.05.18

### Updated
- Update pillow to 9.1.1 ([#3714](https://github.com/cookiecutter/cookiecutter-django/pull/3714))

## 2022.05.16

### Changed
- Update postgres versions ([#3712](https://github.com/cookiecutter/cookiecutter-django/pull/3712))
### Updated
- Update django-anymail to 8.6 ([#3713](https://github.com/cookiecutter/cookiecutter-django/pull/3713))

## 2022.05.14

### Updated
- Update coverage to 6.3.3 ([#3709](https://github.com/cookiecutter/cookiecutter-django/pull/3709))
- Update whitenoise to 6.1.0 ([#3707](https://github.com/cookiecutter/cookiecutter-django/pull/3707))
- Update sentry-sdk to 1.5.12 ([#3706](https://github.com/cookiecutter/cookiecutter-django/pull/3706))
- Update redis to 4.3.1 ([#3704](https://github.com/cookiecutter/cookiecutter-django/pull/3704))

## 2022.05.07

### Changed
- Add pyupgrade to pre-commit config ([#3702](https://github.com/cookiecutter/cookiecutter-django/pull/3702))
- Set permissions for GitHub actions ([#3698](https://github.com/cookiecutter/cookiecutter-django/pull/3698))
### Updated
- Update jinja2 to 3.1.2 ([#3700](https://github.com/cookiecutter/cookiecutter-django/pull/3700))

## 2022.05.06

### Updated
- Update pre-commit to 2.19.0 ([#3697](https://github.com/cookiecutter/cookiecutter-django/pull/3697))

## 2022.05.04

### Updated
- Update django-coverage-plugin to 2.0.3 ([#3695](https://github.com/cookiecutter/cookiecutter-django/pull/3695))

## 2022.05.03

### Updated
- Update django-debug-toolbar to 3.4.0 ([#3692](https://github.com/cookiecutter/cookiecutter-django/pull/3692))
- Update sentry-sdk to 1.5.11 ([#3693](https://github.com/cookiecutter/cookiecutter-django/pull/3693))

## 2022.05.01

### Updated
- Update django-debug-toolbar to 3.3.0 ([#3690](https://github.com/cookiecutter/cookiecutter-django/pull/3690))

## 2022.04.28

### Changed
- Add the possibility to set a max django version on create_django_issue script ([#3680](https://github.com/cookiecutter/cookiecutter-django/pull/3680))

## 2022.04.27

### Updated
- Update mypy to 0.950 ([#3687](https://github.com/cookiecutter/cookiecutter-django/pull/3687))
- Update python-slugify to 6.1.2 ([#3686](https://github.com/cookiecutter/cookiecutter-django/pull/3686))
- Update drf-spectacular to 0.22.1 ([#3684](https://github.com/cookiecutter/cookiecutter-django/pull/3684))

## 2022.04.25

### Updated
- Update pytest to 7.1.2 ([#3683](https://github.com/cookiecutter/cookiecutter-django/pull/3683))

## 2022.04.19

### Updated
- Update tox to 3.25.0 ([#3675](https://github.com/cookiecutter/cookiecutter-django/pull/3675))
- Update sentry-sdk to 1.5.10 ([#3679](https://github.com/cookiecutter/cookiecutter-django/pull/3679))

## 2022.04.13

### Updated
- Bump stefanzweifel/git-auto-commit-action from 4.14.0 to 4.14.1 ([#3677](https://github.com/cookiecutter/cookiecutter-django/pull/3677))

## 2022.04.11

### Updated
- Update django to 3.2.13 ([#3676](https://github.com/cookiecutter/cookiecutter-django/pull/3676))

## 2022.04.08

### Updated
- Auto-update pre-commit hooks ([#3673](https://github.com/cookiecutter/cookiecutter-django/pull/3673))

## 2022.04.05

### Updated
- Update celery to 5.2.6 ([#3671](https://github.com/cookiecutter/cookiecutter-django/pull/3671))

## 2022.04.04

### Updated
- Update redis to 4.2.2 ([#3670](https://github.com/cookiecutter/cookiecutter-django/pull/3670))
- Update celery to 5.2.5 ([#3669](https://github.com/cookiecutter/cookiecutter-django/pull/3669))
- Update pre-commit to 2.18.1 ([#3668](https://github.com/cookiecutter/cookiecutter-django/pull/3668))
- Update pillow to 9.1.0 ([#3665](https://github.com/cookiecutter/cookiecutter-django/pull/3665))

## 2022.04.01

### Changed
- Update domain for Celery docs ([#3663](https://github.com/cookiecutter/cookiecutter-django/pull/3663))
### Updated
- Update watchgod to 0.8.2 ([#3664](https://github.com/cookiecutter/cookiecutter-django/pull/3664))
- Update redis to 4.2.1 ([#3660](https://github.com/cookiecutter/cookiecutter-django/pull/3660))

## 2022.03.28

### Changed
- Update `black` version to `22.3.0` ([#3657](https://github.com/cookiecutter/cookiecutter-django/pull/3657))

## 2022.03.27

### Updated
- Update sphinx to 4.5.0 ([#3654](https://github.com/cookiecutter/cookiecutter-django/pull/3654))
- Update jinja2 to 3.1.1 ([#3652](https://github.com/cookiecutter/cookiecutter-django/pull/3652))
- Update pylint-django to 2.5.3 ([#3650](https://github.com/cookiecutter/cookiecutter-django/pull/3650))
- Update django-allauth to 0.50.0 ([#3649](https://github.com/cookiecutter/cookiecutter-django/pull/3649))
- Update mypy to 0.942 ([#3648](https://github.com/cookiecutter/cookiecutter-django/pull/3648))
- Update jinja2 to 3.1.0 ([#3647](https://github.com/cookiecutter/cookiecutter-django/pull/3647))
- Update redis to 4.2.0 ([#3646](https://github.com/cookiecutter/cookiecutter-django/pull/3646))
- Update watchgod to 0.8.1 ([#3643](https://github.com/cookiecutter/cookiecutter-django/pull/3643))
- Bump stefanzweifel/git-auto-commit-action from 4.13.1 to 4.14.0 ([#3641](https://github.com/cookiecutter/cookiecutter-django/pull/3641))
- Update drf-spectacular to 0.22.0 ([#3642](https://github.com/cookiecutter/cookiecutter-django/pull/3642))
- Update pytz to 2022.1 ([#3639](https://github.com/cookiecutter/cookiecutter-django/pull/3639))
- Update sentry-sdk to 1.5.8 ([#3638](https://github.com/cookiecutter/cookiecutter-django/pull/3638))
- Update pytest to 7.1.1 ([#3637](https://github.com/cookiecutter/cookiecutter-django/pull/3637))
- Update uvicorn to 0.17.6 ([#3627](https://github.com/cookiecutter/cookiecutter-django/pull/3627))

## 2022.03.23

### Updated
- Bump peter-evans/create-pull-request from 3.14.0 to 4 ([#3645](https://github.com/cookiecutter/cookiecutter-django/pull/3645))

## 2022.03.20

### Changed
- Unify compressor, gulp and custom bootstrap options ([#3535](https://github.com/cookiecutter/cookiecutter-django/pull/3535))

## 2022.03.14

### Fixed
- Fix broken link in README of generated projects ([#3634](https://github.com/cookiecutter/cookiecutter-django/pull/3634))

## 2022.03.13

### Changed
- Add DRF spectacular link in requirements ([#3630](https://github.com/cookiecutter/cookiecutter-django/pull/3630))

## 2022.03.09

### Changed
- Fix a few typos in the documentation ([#3625](https://github.com/cookiecutter/cookiecutter-django/pull/3625))

## 2022.03.08

### Updated
- Update sentry-sdk to 1.5.7 ([#3624](https://github.com/cookiecutter/cookiecutter-django/pull/3624))

## 2022.03.03

### Updated
- Upgrade actions/setup-python to v3 ([#3621](https://github.com/cookiecutter/cookiecutter-django/pull/3621))

## 2022.03.02

### Updated
- Bump actions/checkout from 2 to 3 ([#3619](https://github.com/cookiecutter/cookiecutter-django/pull/3619))

## 2022.03.01

### Updated
- Bump actions/setup-python from 2 to 3 ([#3617](https://github.com/cookiecutter/cookiecutter-django/pull/3617))
- Bump peter-evans/create-pull-request from 3.13.0 to 3.14.0 ([#3618](https://github.com/cookiecutter/cookiecutter-django/pull/3618))

## 2022.02.28

### Updated
- Update python-slugify to 6.1.1 ([#3615](https://github.com/cookiecutter/cookiecutter-django/pull/3615))
- Bump peter-evans/create-pull-request from 3.12.1 to 3.13.0 ([#3616](https://github.com/cookiecutter/cookiecutter-django/pull/3616))

## 2022.02.25

### Updated
- Bump actions/setup-node from 2 to 3 ([#3614](https://github.com/cookiecutter/cookiecutter-django/pull/3614))

## 2022.02.24

### Updated
- Update django-allauth to 0.49.0 ([#3613](https://github.com/cookiecutter/cookiecutter-django/pull/3613))
- Update sentry-sdk to 1.5.6 ([#3611](https://github.com/cookiecutter/cookiecutter-django/pull/3611))
- Update python-slugify to 6.1.0 ([#3612](https://github.com/cookiecutter/cookiecutter-django/pull/3612))

## 2022.02.21

### Changed
- Cancel previous CI runs on successive PR pushes with GitHub actions ([#3575](https://github.com/cookiecutter/cookiecutter-django/pull/3575))
### Updated
- Update coverage to 6.3.2 ([#3610](https://github.com/cookiecutter/cookiecutter-django/pull/3610))
- Update gitpython to 3.1.27 ([#3607](https://github.com/cookiecutter/cookiecutter-django/pull/3607))
- Update pylint-django to 2.5.2 ([#3602](https://github.com/cookiecutter/cookiecutter-django/pull/3602))
- Update python-slugify to 6.0.1 ([#3599](https://github.com/cookiecutter/cookiecutter-django/pull/3599))
- Update uvicorn to 0.17.5 ([#3596](https://github.com/cookiecutter/cookiecutter-django/pull/3596))
- Update redis to 4.1.4 ([#3595](https://github.com/cookiecutter/cookiecutter-django/pull/3595))

## 2022.02.20

### Changed
- Fix incorrect createdb instruction in documentation ([#3606](https://github.com/cookiecutter/cookiecutter-django/pull/3606))

## 2022.02.16

### Fixed
- Fix Swagger schema API endpoint &amp; add a test for it ([#3592](https://github.com/cookiecutter/cookiecutter-django/pull/3592))

## 2022.02.15

### Changed
- Update the drf-spectacular local dev server url to use http instead of https ([#3591](https://github.com/cookiecutter/cookiecutter-django/pull/3591))

## 2022.02.13

### Changed
- Change docs port from 7000 to 9000 ([#3590](https://github.com/cookiecutter/cookiecutter-django/pull/3590))

## 2022.02.12

### Updated
- Update pytest to 7.0.1 ([#3588](https://github.com/cookiecutter/cookiecutter-django/pull/3588))

## 2022.02.11

### Updated
- Update sentry-sdk to 1.5.5 ([#3586](https://github.com/cookiecutter/cookiecutter-django/pull/3586))

## 2022.02.10

### Fixed
- Fix GitLab CI error caused by Docker Compose&#39;s `platform` option ([#3585](https://github.com/cookiecutter/cookiecutter-django/pull/3585))
### Updated
- Update whitenoise to 6.0.0 ([#3583](https://github.com/cookiecutter/cookiecutter-django/pull/3583))

## 2022.02.08

### Fixed
- Fixed some typos in drf-spectacular description and comments ([#3579](https://github.com/cookiecutter/cookiecutter-django/pull/3579))
### Updated
- Update redis to 4.1.3 ([#3577](https://github.com/cookiecutter/cookiecutter-django/pull/3577))
- Update werkzeug to 2.0.3 ([#3576](https://github.com/cookiecutter/cookiecutter-django/pull/3576))

## 2022.02.07

### Changed
- Update black to 22.1.0 ([#3572](https://github.com/cookiecutter/cookiecutter-django/pull/3572))
### Fixed
- Fix docker-compose config on Apple silicon ([#3562](https://github.com/cookiecutter/cookiecutter-django/pull/3562))
### Updated
- Update uvicorn to 0.17.4 ([#3574](https://github.com/cookiecutter/cookiecutter-django/pull/3574))
- Update django-allauth to 0.48.0 ([#3573](https://github.com/cookiecutter/cookiecutter-django/pull/3573))
- Update pytest to 7.0.0 ([#3567](https://github.com/cookiecutter/cookiecutter-django/pull/3567))
- Update coverage to 6.3.1 ([#3561](https://github.com/cookiecutter/cookiecutter-django/pull/3561))
- Update pillow to 9.0.1 ([#3571](https://github.com/cookiecutter/cookiecutter-django/pull/3571))
- Bump peter-evans/create-pull-request from 3.12.0 to 3.12.1 ([#3558](https://github.com/cookiecutter/cookiecutter-django/pull/3558))
- Update drf-spectacular to 0.21.2 ([#3560](https://github.com/cookiecutter/cookiecutter-django/pull/3560))
- Update django to 3.2.12 ([#3559](https://github.com/cookiecutter/cookiecutter-django/pull/3559))

## 2022.01.27

### Updated
- Update redis to 4.1.2 ([#3551](https://github.com/cookiecutter/cookiecutter-django/pull/3551))

## 2022.01.26

### Updated
- Update coverage to 6.3 ([#3550](https://github.com/cookiecutter/cookiecutter-django/pull/3550))
- Update sentry-sdk to 1.5.4 ([#3549](https://github.com/cookiecutter/cookiecutter-django/pull/3549))
- Update django-crispy-forms to 1.14.0 ([#3548](https://github.com/cookiecutter/cookiecutter-django/pull/3548))
- Update uvicorn to 0.17.0.post1 ([#3547](https://github.com/cookiecutter/cookiecutter-django/pull/3547))

## 2022.01.21

### Changed
- mysql support link ([#3544](https://github.com/cookiecutter/cookiecutter-django/pull/3544))
### Updated
- Update sentry-sdk to 1.5.3 ([#3543](https://github.com/cookiecutter/cookiecutter-django/pull/3543))
- Update django-anymail to 8.5 ([#3542](https://github.com/cookiecutter/cookiecutter-django/pull/3542))

## 2022.01.19

### Changed
- Add swagger API documentation when DRF is enabled  ([#3536](https://github.com/cookiecutter/cookiecutter-django/pull/3536))
### Updated
- Update pre-commit to 2.17.0 ([#3541](https://github.com/cookiecutter/cookiecutter-django/pull/3541))

## 2022.01.17

### Changed
- Avoid docker image/volume collision by prefixing with project slug ([#3528](https://github.com/cookiecutter/cookiecutter-django/pull/3528))
### Updated
- Update redis to 4.1.1 ([#3540](https://github.com/cookiecutter/cookiecutter-django/pull/3540))
- Update sphinx to 4.4.0 ([#3537](https://github.com/cookiecutter/cookiecutter-django/pull/3537))

## 2022.01.14

### Updated
- Update uvicorn to 0.17.0 ([#3534](https://github.com/cookiecutter/cookiecutter-django/pull/3534))
- Bump stefanzweifel/git-auto-commit-action from 4.13.0 to 4.13.1 ([#3532](https://github.com/cookiecutter/cookiecutter-django/pull/3532))

## 2022.01.13

### Changed
- Add UserSignupForm and UserSocialSignupForm ([#3515](https://github.com/cookiecutter/cookiecutter-django/pull/3515))
### Fixed
- Fix high CPU usage when running `runserver_plus` in Docker ([#3531](https://github.com/cookiecutter/cookiecutter-django/pull/3531))
- Fix out-of-sync sequence for Site ID ([#3511](https://github.com/cookiecutter/cookiecutter-django/pull/3511))

## 2022.01.11

### Updated
- Bump stefanzweifel/git-auto-commit-action from 4.12.0 to 4.13.0 ([#3527](https://github.com/cookiecutter/cookiecutter-django/pull/3527))

## 2022.01.10

### Updated
- Update django-cors-headers to 3.11.0 ([#3526](https://github.com/cookiecutter/cookiecutter-django/pull/3526))
- Update sentry-sdk to 1.5.2 ([#3525](https://github.com/cookiecutter/cookiecutter-django/pull/3525))
- Update gitpython to 3.1.26 ([#3524](https://github.com/cookiecutter/cookiecutter-django/pull/3524))

## 2022.01.09

### Changed
- Fix broken center align of image links in README  ([#3522](https://github.com/cookiecutter/cookiecutter-django/pull/3522))

## 2022.01.07

### Fixed
- Fix cache dependency path for linter job in CI workflow ([#3520](https://github.com/cookiecutter/cookiecutter-django/pull/3520))
- Fix `open` option for `initBrowserSync` when using Docker ([#3519](https://github.com/cookiecutter/cookiecutter-django/pull/3519))
### Updated
- Update mypy to 0.931 ([#3521](https://github.com/cookiecutter/cookiecutter-django/pull/3521))
- Update gitpython to 3.1.25 ([#3518](https://github.com/cookiecutter/cookiecutter-django/pull/3518))

## 2022.01.06

### Changed
- Update output example in README ([#3512](https://github.com/cookiecutter/cookiecutter-django/pull/3512))

## 2022.01.05

### Changed
- Update references to Bootstrap from v4 to v5 in README ([#3513](https://github.com/cookiecutter/cookiecutter-django/pull/3513))
### Updated
- Update requests to 2.27.1 ([#3516](https://github.com/cookiecutter/cookiecutter-django/pull/3516))

## 2022.01.04

### Changed
- Double quote array expansions to avoid re-splitting elements ([#3514](https://github.com/cookiecutter/cookiecutter-django/pull/3514))
### Updated
- Update django to 3.2.11 ([#3510](https://github.com/cookiecutter/cookiecutter-django/pull/3510))

## 2022.01.03

### Changed
- Convert top level RST files to Markdown ([#3489](https://github.com/cookiecutter/cookiecutter-django/pull/3489))
### Updated
- Update requests to 2.27.0 ([#3509](https://github.com/cookiecutter/cookiecutter-django/pull/3509))
- Update pillow to 9.0.0 ([#3508](https://github.com/cookiecutter/cookiecutter-django/pull/3508))
- Update pylint-django to 2.5.0 ([#3505](https://github.com/cookiecutter/cookiecutter-django/pull/3505))

## 2021.12.29

### Fixed
- Add generated files to `.gitignore` when selecting Gulp ([#3500](https://github.com/cookiecutter/cookiecutter-django/pull/3500))
### Updated
- Update psycopg2-binary to 2.9.3 ([#3504](https://github.com/cookiecutter/cookiecutter-django/pull/3504))
- Update psycopg2 to 2.9.3 ([#3503](https://github.com/cookiecutter/cookiecutter-django/pull/3503))
- Update celery to 5.2.3 ([#3502](https://github.com/cookiecutter/cookiecutter-django/pull/3502))
- Update tox to 3.24.5 ([#3501](https://github.com/cookiecutter/cookiecutter-django/pull/3501))

## 2021.12.28

### Changed
- Build the HTML for the documentation as part of the CI ([#3498](https://github.com/cookiecutter/cookiecutter-django/pull/3498))

## 2021.12.27

### Changed
- Hides &#39;sign up&#39; elements when ACCOUNT_ALLOW_REGISTRATION is disabled ([#1914](https://github.com/cookiecutter/cookiecutter-django/pull/1914))

## 2021.12.26

### Fixed
- Fix missing psycopg2 dependency in docs Docker image ([#3494](https://github.com/cookiecutter/cookiecutter-django/pull/3494))
### Updated
- Update celery to 5.2.2 ([#3496](https://github.com/cookiecutter/cookiecutter-django/pull/3496))
- Update redis to 4.1.0 ([#3495](https://github.com/cookiecutter/cookiecutter-django/pull/3495))

## 2021.12.25

### Changed
- Automatically add Django version label to issue ([#3492](https://github.com/cookiecutter/cookiecutter-django/pull/3492))
### Updated
- Auto-update pre-commit hooks ([#3493](https://github.com/cookiecutter/cookiecutter-django/pull/3493))

## 2021.12.24

### Changed
- Simplify `TEMPLATES` settings with `APP_DIRS=True` ([#3488](https://github.com/cookiecutter/cookiecutter-django/pull/3488))
- Fix docs not building ([#3491](https://github.com/cookiecutter/cookiecutter-django/pull/3491))
- Remove pylint-django from VITAL_BUT_UNKNOWN ([#3490](https://github.com/cookiecutter/cookiecutter-django/pull/3490))
- Making docs image 40% smaller and also making python version upgrades easier for multi-stage builds. ([#2836](https://github.com/cookiecutter/cookiecutter-django/pull/2836))
- Added Django&#39;s current language to the lang attribute of the html tag ([#3174](https://github.com/cookiecutter/cookiecutter-django/pull/3174))
### Updated
- Update uvicorn to 0.16.0 ([#3454](https://github.com/cookiecutter/cookiecutter-django/pull/3454))

## 2021.12.22

### Changed
- Use built-in pip caching from actions/setup-python in generated project ([#3481](https://github.com/cookiecutter/cookiecutter-django/pull/3481))
- Speed up CI tests on macOS ([#3480](https://github.com/cookiecutter/cookiecutter-django/pull/3480))
### Updated
- Update mypy to 0.930 ([#3487](https://github.com/cookiecutter/cookiecutter-django/pull/3487))
- Update redis to 4.0.2 ([#3486](https://github.com/cookiecutter/cookiecutter-django/pull/3486))
- Update django-redis to 5.2.0 ([#3485](https://github.com/cookiecutter/cookiecutter-django/pull/3485))

## 2021.12.20

### Changed
- Add a PyCharm run configuration for docker-compose ([#3462](https://github.com/cookiecutter/cookiecutter-django/pull/3462))

## 2021.12.19

### Updated
- Update mypy to 0.920 ([#3478](https://github.com/cookiecutter/cookiecutter-django/pull/3478))
- Update django-compressor to 3.1 ([#3476](https://github.com/cookiecutter/cookiecutter-django/pull/3476))
- Update sphinx to 4.3.2 ([#3477](https://github.com/cookiecutter/cookiecutter-django/pull/3477))

## 2021.12.17

### Fixed
- Fix BrowserSync config on non-Docker setup ([#3461](https://github.com/cookiecutter/cookiecutter-django/pull/3461))

## 2021.12.16

### Fixed
- Fix carriage return in `.gitignore` on Windows ([#3456](https://github.com/cookiecutter/cookiecutter-django/pull/3456))
### Updated
- Update django-debug-toolbar to 3.2.4 ([#3473](https://github.com/cookiecutter/cookiecutter-django/pull/3473))

## 2021.12.15

### Updated
- Update djangorestframework to 3.13.1 ([#3472](https://github.com/cookiecutter/cookiecutter-django/pull/3472))

## 2021.12.14

### Changed
- Update rcssmin &amp; django-compressor ([#3470](https://github.com/cookiecutter/cookiecutter-django/pull/3470))
### Updated
- Update pytest-django to 4.5.2 ([#3471](https://github.com/cookiecutter/cookiecutter-django/pull/3471))
- Bump peter-evans/create-pull-request from 3.11.0 to 3.12.0 ([#3469](https://github.com/cookiecutter/cookiecutter-django/pull/3469))

## 2021.12.13

### Updated
- Update djangorestframework to 3.13.0 ([#3468](https://github.com/cookiecutter/cookiecutter-django/pull/3468))
- Update sentry-sdk to 1.5.1 ([#3467](https://github.com/cookiecutter/cookiecutter-django/pull/3467))
- Update django-debug-toolbar to 3.2.3 ([#3466](https://github.com/cookiecutter/cookiecutter-django/pull/3466))
- Update argon2-cffi to 21.3.0 ([#3464](https://github.com/cookiecutter/cookiecutter-django/pull/3464))
- Update django-allauth to 0.47.0 ([#3459](https://github.com/cookiecutter/cookiecutter-django/pull/3459))

## 2021.12.09

### Updated
- Auto-update pre-commit hooks ([#3457](https://github.com/cookiecutter/cookiecutter-django/pull/3457))

## 2021.12.08

### Changed
- Reword introduction in documentation ([#3452](https://github.com/cookiecutter/cookiecutter-django/pull/3452))
### Updated
- Update argon2-cffi to 21.2.0 ([#3453](https://github.com/cookiecutter/cookiecutter-django/pull/3453))

## 2021.12.07

### Changed
- Add docker, pip and npm to GitHub&#39;s Dependabot ([#3401](https://github.com/cookiecutter/cookiecutter-django/pull/3401))
- Configure Dependabot for npm packages at the template level ([#3436](https://github.com/cookiecutter/cookiecutter-django/pull/3436))
### Updated
- Update django to 3.2.10 ([#3451](https://github.com/cookiecutter/cookiecutter-django/pull/3451))

## 2021.12.06

### Updated
- Auto-update pre-commit hooks ([#3449](https://github.com/cookiecutter/cookiecutter-django/pull/3449))
- Update black to 21.12b0 ([#3448](https://github.com/cookiecutter/cookiecutter-django/pull/3448))
- Update django-cors-headers to 3.10.1 ([#3447](https://github.com/cookiecutter/cookiecutter-django/pull/3447))

## 2021.12.04

### Changed
- Removed mention of Foundation fork from readme ([#3445](https://github.com/cookiecutter/cookiecutter-django/pull/3445))
### Updated
- Update pytest-django to 4.5.1 ([#3443](https://github.com/cookiecutter/cookiecutter-django/pull/3443))

## 2021.12.01

### Updated
- Update pre-commit to 2.16.0 ([#3442](https://github.com/cookiecutter/cookiecutter-django/pull/3442))

## 2021.11.30

### Updated
- Update django-redis to 5.1.0 ([#3440](https://github.com/cookiecutter/cookiecutter-django/pull/3440))
- Update django-stubs to 1.9.0 ([#3439](https://github.com/cookiecutter/cookiecutter-django/pull/3439))

## 2021.11.29

### Fixed
- Fix pre-commit config ([#3435](https://github.com/cookiecutter/cookiecutter-django/pull/3435))
### Updated
- Update sphinx to 4.3.1 ([#3438](https://github.com/cookiecutter/cookiecutter-django/pull/3438))

## 2021.11.27

### Updated
- Update coverage to 6.2 ([#3437](https://github.com/cookiecutter/cookiecutter-django/pull/3437))

## 2021.11.26

### Changed
- Setup pre-commit for the template files ([#3433](https://github.com/cookiecutter/cookiecutter-django/pull/3433))

## 2021.11.25

### Changed
- Add an assertion to fix mypy type error ([#3150](https://github.com/cookiecutter/cookiecutter-django/pull/3150))
- Make `django` depend on `redis` in local Docker  ([#3265](https://github.com/cookiecutter/cookiecutter-django/pull/3265))

## 2021.11.24

### Changed
- Cache Python dependencies on our CI ([#3434](https://github.com/cookiecutter/cookiecutter-django/pull/3434))
- Small formatting fixes to Deploy to PythonAnywhere page ([#3432](https://github.com/cookiecutter/cookiecutter-django/pull/3432))
### Updated
- Upgrade to Django 3.2 ([#3425](https://github.com/cookiecutter/cookiecutter-django/pull/3425))

## 2021.11.22

### Changed
- Removed unnecessary custom context processor exposing the DEBUG Template Context Variable ([#3042](https://github.com/cookiecutter/cookiecutter-django/pull/3042))
- Clean up trailing whitespace ([#3430](https://github.com/cookiecutter/cookiecutter-django/pull/3430))
### Updated
- Update redis to 4.0.2 ([#3431](https://github.com/cookiecutter/cookiecutter-django/pull/3431))
- Bump Postgres to 13.5 12.9 11.14 10.19; add 14.1 ([#3428](https://github.com/cookiecutter/cookiecutter-django/pull/3428))

## 2021.11.20

### Fixed
- Update repos for pre-commit hooks ([#3424](https://github.com/cookiecutter/cookiecutter-django/pull/3424))
### Updated
- Bump pre-commit/action to 2.0.3 ([#3426](https://github.com/cookiecutter/cookiecutter-django/pull/3426))

## 2021.11.19

### Updated
- Update celery to 5.2.1 ([#3423](https://github.com/cookiecutter/cookiecutter-django/pull/3423))
- Auto-update pre-commit hooks ([#3420](https://github.com/cookiecutter/cookiecutter-django/pull/3420))

## 2021.11.18

### Changed
- Switch template to calendar versioning &amp; automate releases ([#3415](https://github.com/cookiecutter/cookiecutter-django/pull/3415))
### Updated
- Update black to 21.11b1 ([#3421](https://github.com/cookiecutter/cookiecutter-django/pull/3421))
- Update redis to 4.0.1 ([#3416](https://github.com/cookiecutter/cookiecutter-django/pull/3416))

## [2021-11-17]
### Updated
- Update sentry-sdk to 1.5.0 ([#3417](https://github.com/cookiecutter/cookiecutter-django/pull/3417))
- Update black to 21.11b0 ([#3414](https://github.com/cookiecutter/cookiecutter-django/pull/3414))

## [2021-11-16]
### Changed
- Upgrade JS dependencies and upgrade to node 16 ([#3400](https://github.com/cookiecutter/cookiecutter-django/pull/3400))
### Fixed
- Fix ungraceful Celery workers shutdown in container ([#3405](https://github.com/cookiecutter/cookiecutter-django/pull/3405))
### Updated
- Update psycopg2-binary to 2.9.2 ([#3411](https://github.com/cookiecutter/cookiecutter-django/pull/3411))
- Update psycopg2 to 2.9.2 ([#3410](https://github.com/cookiecutter/cookiecutter-django/pull/3410))
- Update redis to 4.0.0 ([#3406](https://github.com/cookiecutter/cookiecutter-django/pull/3406))
- Update django-coverage-plugin to 2.0.2 ([#3409](https://github.com/cookiecutter/cookiecutter-django/pull/3409))
- Update black to 21.10b0 ([#3408](https://github.com/cookiecutter/cookiecutter-django/pull/3408))

## [2021-11-15]
### Updated
- Update django-allauth to 0.46.0 ([#3407](https://github.com/cookiecutter/cookiecutter-django/pull/3407))

## [2021-11-13]
### Fixed
- Fix incorrect node version in `package.json` ([#3399](https://github.com/cookiecutter/cookiecutter-django/pull/3399))

## [2021-11-12]
### Changed
- Add Django major/minor release table maker in GitHub issues ([#3288](https://github.com/cookiecutter/cookiecutter-django/pull/3288))
- Upgrade to Bootstrap 5 ([#3276](https://github.com/cookiecutter/cookiecutter-django/pull/3276))
### Updated
- Update requests to 2.26.0 ([#3397](https://github.com/cookiecutter/cookiecutter-django/pull/3397))
- Update crispy-bootstrap5 to 0.6 ([#3396](https://github.com/cookiecutter/cookiecutter-django/pull/3396))

## [2021-11-11]
### Changed
- Build all images on CI ([#3394](https://github.com/cookiecutter/cookiecutter-django/pull/3394))
### Updated
- Update coverage to 6.1.2 ([#3393](https://github.com/cookiecutter/cookiecutter-django/pull/3393))

## [2021-11-10]
### Changed
- Update sphinx to 4.3.0 ([#3392](https://github.com/cookiecutter/cookiecutter-django/pull/3392))
### Updated
- Auto-update pre-commit hooks ([#3389](https://github.com/cookiecutter/cookiecutter-django/pull/3389))
- Update jinja2 to 3.0.3 ([#3388](https://github.com/cookiecutter/cookiecutter-django/pull/3388))

## [2021-11-09]
### Changed
- refactor: remove user API methods parameter ([#3385](https://github.com/cookiecutter/cookiecutter-django/pull/3385))
- Get GitHub repo from environment ([#3387](https://github.com/cookiecutter/cookiecutter-django/pull/3387))
### Updated
- Update celery to 5.2.0 ([#3384](https://github.com/cookiecutter/cookiecutter-django/pull/3384))
- Update isort to 5.10.1 ([#3386](https://github.com/cookiecutter/cookiecutter-django/pull/3386))

## [2021-11-08]
### Changed
- Update docker and non-docker configs to Debian 11 (bullseye) ([#3372](https://github.com/cookiecutter/cookiecutter-django/pull/3372))

## [2021-11-07]
### Updated
- Update django-extensions to 3.1.5 ([#3383](https://github.com/cookiecutter/cookiecutter-django/pull/3383))

## [2021-11-04]
### Changed
- change path in docs Makefile to use APP variable ([#3379](https://github.com/cookiecutter/cookiecutter-django/pull/3379))
### Fixed
- fix help in docs Makefile ([#3380](https://github.com/cookiecutter/cookiecutter-django/pull/3380))
### Updated
- Bump peter-evans/create-pull-request from 3.10.1 to 3.11.0 ([#3382](https://github.com/cookiecutter/cookiecutter-django/pull/3382))
- Auto-update pre-commit hooks ([#3381](https://github.com/cookiecutter/cookiecutter-django/pull/3381))
- Update isort to 5.10.0 ([#3378](https://github.com/cookiecutter/cookiecutter-django/pull/3378))

## [2021-11-02]
### Updated
- Auto-update pre-commit hooks ([#3377](https://github.com/cookiecutter/cookiecutter-django/pull/3377))

## [2021-11-01]
### Updated
- Update django-storages to 1.12.3 ([#3374](https://github.com/cookiecutter/cookiecutter-django/pull/3374))
- Update coverage to 6.1.1 ([#3376](https://github.com/cookiecutter/cookiecutter-django/pull/3376))

## [2021-10-28]
### Updated
- Update factory-boy to 3.2.1 ([#3373](https://github.com/cookiecutter/cookiecutter-django/pull/3373))

## [2021-10-26]
### Changed
- use Wayback Machine to fix dead link for postgres user setup ([#3363](https://github.com/cookiecutter/cookiecutter-django/pull/3363))
- Fix pull request links to correct repo URL on CHANGELOG.md  ([#3370](https://github.com/cookiecutter/cookiecutter-django/pull/3370))
### Updated
- Update pyyaml to 6.0 ([#3362](https://github.com/cookiecutter/cookiecutter-django/pull/3362))
- Update pillow to 8.4.0 ([#3364](https://github.com/cookiecutter/cookiecutter-django/pull/3364))
- Update django-storages to 1.12.2 ([#3365](https://github.com/cookiecutter/cookiecutter-django/pull/3365))
- Update django-environ to 0.8.1 ([#3368](https://github.com/cookiecutter/cookiecutter-django/pull/3368))

## [2021-10-22]
### Changed
- Move repo under cookiecutter organisation ([#3357](https://github.com/cookiecutter/cookiecutter-django/pull/3357))

## [2021-10-18]
### Updated
- Update django-environ to 0.8.0 ([#3367](https://github.com/cookiecutter/cookiecutter-django/pull/3367))

## [2021-10-14]
### Updated
- Update flake8 to 4.0.1 ([#3361](https://github.com/cookiecutter/cookiecutter-django/pull/3361))
- Update flake8-isort to 4.1.1 ([#3360](https://github.com/cookiecutter/cookiecutter-django/pull/3360))
- Update django-model-utils to 4.2.0 ([#3359](https://github.com/cookiecutter/cookiecutter-django/pull/3359))

## [2021-10-13]
### Changed
- Add drf stubs ([#3353](https://github.com/cookiecutter/cookiecutter-django/pull/3353))

## [2021-10-12]
### Updated
- Update coverage to 6.0.2 ([#3356](https://github.com/cookiecutter/cookiecutter-django/pull/3356))

## [2021-10-11]
### Updated
- Update werkzeug to 2.0.2 ([#3344](https://github.com/cookiecutter/cookiecutter-django/pull/3344))
- Update coverage to 6.0.1 ([#3348](https://github.com/cookiecutter/cookiecutter-django/pull/3348))
- Update django-coverage-plugin to 2.0.1 ([#3349](https://github.com/cookiecutter/cookiecutter-django/pull/3349))
- Update django-cors-headers to 3.10.0 ([#3345](https://github.com/cookiecutter/cookiecutter-django/pull/3345))
- Update jinja2 to 3.0.2 ([#3343](https://github.com/cookiecutter/cookiecutter-django/pull/3343))
- Update django-storages to 1.12.1 ([#3355](https://github.com/cookiecutter/cookiecutter-django/pull/3355))

## [2021-10-03]
### Updated
- Update pytz to 2021.3 ([#3340](https://github.com/cookiecutter/cookiecutter-django/pull/3340))

## [2021-10-01]
### Changed
- Fix the wrong pre-commit hyperlink in Prerequisites section ([#3338](https://github.com/cookiecutter/cookiecutter-django/pull/3338))

## [2021-09-30]
### Updated
- Update sentry-sdk to 1.4.3 ([#3334](https://github.com/cookiecutter/cookiecutter-django/pull/3334))

## [2021-09-29]
### Updated
- Update django-cors-headers to 3.9.0 ([#3332](https://github.com/cookiecutter/cookiecutter-django/pull/3332))

## [2021-09-27]
### Updated
- Update sentry-sdk to 1.4.2 ([#3329](https://github.com/cookiecutter/cookiecutter-django/pull/3329))

## [2021-09-26]
### Updated
- Update django-crispy-forms to 1.13.0 ([#3327](https://github.com/cookiecutter/cookiecutter-django/pull/3327))

## [2021-09-24]
### Changed
- Add django-settings-module to .pylintrc ([#3326](https://github.com/cookiecutter/cookiecutter-django/pull/3326))

## [2021-09-23]
### Updated
- Update sentry-sdk to 1.4.1 ([#3325](https://github.com/cookiecutter/cookiecutter-django/pull/3325))

## [2021-09-22]
### Updated
- Update sentry-sdk to 1.4.0 ([#3324](https://github.com/cookiecutter/cookiecutter-django/pull/3324))

## [2021-09-16]
### Updated
- Update tox to 3.24.4 ([#3323](https://github.com/cookiecutter/cookiecutter-django/pull/3323))

## [2021-09-15]
### Updated
- Auto-update pre-commit hooks ([#3322](https://github.com/cookiecutter/cookiecutter-django/pull/3322))

## [2021-09-14]
### Updated
- Update black to 21.9b0 ([#3321](https://github.com/cookiecutter/cookiecutter-django/pull/3321))

## [2021-09-13]
### Updated
- Bump stefanzweifel/git-auto-commit-action from 4.11.0 to 4.12.0 ([#3320](https://github.com/cookiecutter/cookiecutter-django/pull/3320))
- Update sphinx to 4.2.0 ([#3319](https://github.com/cookiecutter/cookiecutter-django/pull/3319))

## [2021-09-11]
### Changed
- Removing pycharm docs if app does not use pycharm ([#3139](https://github.com/cookiecutter/cookiecutter-django/pull/3139))
### Updated
- Update django-environ to 0.7.0 ([#3317](https://github.com/cookiecutter/cookiecutter-django/pull/3317))

## [2021-09-06]
### Changed
- Update Celery to v5 ([#3280](https://github.com/cookiecutter/cookiecutter-django/pull/3280))

## [2021-09-05]
### Updated
- Update django-environ to 0.6.0 ([#3314](https://github.com/cookiecutter/cookiecutter-django/pull/3314))

## [2021-09-03]
### Changed
- Update available postgres versions ([#3297](https://github.com/cookiecutter/cookiecutter-django/pull/3297))
### Updated
- Update pre-commit to 2.15.0 ([#3313](https://github.com/cookiecutter/cookiecutter-django/pull/3313))
- Auto-update pre-commit hooks ([#3307](https://github.com/cookiecutter/cookiecutter-django/pull/3307))
- Update pillow to 8.3.2 ([#3312](https://github.com/cookiecutter/cookiecutter-django/pull/3312))
- Update django-environ to 0.5.0 ([#3311](https://github.com/cookiecutter/cookiecutter-django/pull/3311))
- Update pytest to 6.2.5 ([#3310](https://github.com/cookiecutter/cookiecutter-django/pull/3310))
- Update black to 21.8b0 ([#3308](https://github.com/cookiecutter/cookiecutter-django/pull/3308))
- Update argon2-cffi to 21.1.0 ([#3306](https://github.com/cookiecutter/cookiecutter-django/pull/3306))
- Bump peter-evans/create-pull-request from 3.10.0 to 3.10.1 ([#3303](https://github.com/cookiecutter/cookiecutter-django/pull/3303))
- Update django-debug-toolbar to 3.2.2 ([#3296](https://github.com/cookiecutter/cookiecutter-django/pull/3296))
- Update django-cors-headers to 3.8.0 ([#3295](https://github.com/cookiecutter/cookiecutter-django/pull/3295))
- Update uvicorn to 0.15.0 ([#3294](https://github.com/cookiecutter/cookiecutter-django/pull/3294))

## [2021-08-27]
### Updated
- Update tox to 3.24.3 ([#3302](https://github.com/cookiecutter/cookiecutter-django/pull/3302))

## [2021-08-20]
### Changed
- Fix Jinja2 break line control on Procfile ([#3300](https://github.com/cookiecutter/cookiecutter-django/pull/3300))

## [2021-08-19]
### Changed
- Fix several minor typos ([#3301](https://github.com/cookiecutter/cookiecutter-django/pull/3301))

## [2021-08-13]
### Changed
- Upgrade to Redis 6 ([#3255](https://github.com/cookiecutter/cookiecutter-django/pull/3255))
### Fixed
- Fix RTD build image to support Python 3.9 ([#3293](https://github.com/cookiecutter/cookiecutter-django/pull/3293))

## [2021-08-12]
### Changed
- Add documentation for automating backups ([#3268](https://github.com/cookiecutter/cookiecutter-django/pull/3268))
- Add missing step to getting started locally in docs ([#3291](https://github.com/cookiecutter/cookiecutter-django/pull/3291))
- Moved isort config from `.editorconfig` to `setup.cfg` ([#3290](https://github.com/cookiecutter/cookiecutter-django/pull/3290))
- How to pre-commit in Docker Development ([#3287](https://github.com/cookiecutter/cookiecutter-django/pull/3287))
### Updated
- Update sentry-sdk to 1.3.1 ([#3281](https://github.com/cookiecutter/cookiecutter-django/pull/3281))
- Update tox to 3.24.1 ([#3285](https://github.com/cookiecutter/cookiecutter-django/pull/3285))
- Update pre-commit to 2.14.0 ([#3289](https://github.com/cookiecutter/cookiecutter-django/pull/3289))

## [2021-07-30]
### Updated
- Auto-update pre-commit hooks ([#3283](https://github.com/cookiecutter/cookiecutter-django/pull/3283))
- Update isort to 5.9.3 ([#3282](https://github.com/cookiecutter/cookiecutter-django/pull/3282))

## [2021-07-27]
### Changed
- Convert trans to translate in templates ([#3277](https://github.com/cookiecutter/cookiecutter-django/pull/3277))
### Updated
- Update hiredis to 2.0.0 ([#3110](https://github.com/cookiecutter/cookiecutter-django/pull/3110))
- Update mypy to 0.910 ([#3237](https://github.com/cookiecutter/cookiecutter-django/pull/3237))
- Update whitenoise to 5.3.0 ([#3273](https://github.com/cookiecutter/cookiecutter-django/pull/3273))
- Update tox to 3.24.0 ([#3269](https://github.com/cookiecutter/cookiecutter-django/pull/3269))
- Update django-allauth to 0.45.0 ([#3267](https://github.com/cookiecutter/cookiecutter-django/pull/3267))
- Update sentry-sdk to 1.3.0 ([#3262](https://github.com/cookiecutter/cookiecutter-django/pull/3262))
- Update sphinx to 4.1.2 ([#3278](https://github.com/cookiecutter/cookiecutter-django/pull/3278))
- Auto-update pre-commit hooks ([#3264](https://github.com/cookiecutter/cookiecutter-django/pull/3264))
- Update isort to 5.9.2 ([#3279](https://github.com/cookiecutter/cookiecutter-django/pull/3279))
- Update pillow to 8.3.1 ([#3259](https://github.com/cookiecutter/cookiecutter-django/pull/3259))
- Update black to 21.7b0 ([#3272](https://github.com/cookiecutter/cookiecutter-django/pull/3272))

## [2021-07-12]
### Changed
- Define REMAP_SIGTERM=SIGQUIT on Profile of Celery on Heroku ([#3263](https://github.com/cookiecutter/cookiecutter-django/pull/3263))

## [2021-07-08]
### Updated
- Update django to 3.1.13 ([#3247](https://github.com/cookiecutter/cookiecutter-django/pull/3247))

## [2021-06-29]
### Changed
- Improve github bug report template ([#3243](https://github.com/cookiecutter/cookiecutter-django/pull/3243))

## [2021-06-28]
### Changed
- Revert &#34;Fix Celery ports error on local Docker&#34; ([#3242](https://github.com/cookiecutter/cookiecutter-django/pull/3242))
### Fixed
- Fix Celery ports error on local Docker ([#3241](https://github.com/cookiecutter/cookiecutter-django/pull/3241))

## [2021-06-25]
### Changed
- Update `.gitignore` file for VSCode ([#3238](https://github.com/cookiecutter/cookiecutter-django/pull/3238))
### Fixed
- Wrap jQuery call in `DOMContentLoaded` event listener on account email page ([#3239](https://github.com/cookiecutter/cookiecutter-django/pull/3239))

## [2021-06-22]
### Changed
- Update docs/howto.rst ([#3230](https://github.com/cookiecutter/cookiecutter-django/pull/3230))
- Add support for PG 13. Drop PG 9. Update all minor versions ([#3154](https://github.com/cookiecutter/cookiecutter-django/pull/3154))
### Updated
- Update isort to 5.9.1 ([#3236](https://github.com/cookiecutter/cookiecutter-django/pull/3236))
- Auto-update pre-commit hooks ([#3235](https://github.com/cookiecutter/cookiecutter-django/pull/3235))

## [2021-06-21]
### Updated
- Update isort to 5.9.0 ([#3234](https://github.com/cookiecutter/cookiecutter-django/pull/3234))
- Update django-anymail to 8.4 ([#3225](https://github.com/cookiecutter/cookiecutter-django/pull/3225))
- Update django-redis to 5.0.0 ([#3205](https://github.com/cookiecutter/cookiecutter-django/pull/3205))
- Update pylint-django to 2.4.4 ([#3233](https://github.com/cookiecutter/cookiecutter-django/pull/3233))
- Auto-update pre-commit hooks ([#3220](https://github.com/cookiecutter/cookiecutter-django/pull/3220))
- Bump peter-evans/create-pull-request from 3.9.2 to 3.10.0 ([#3197](https://github.com/cookiecutter/cookiecutter-django/pull/3197))
- Update black to 21.6b0 ([#3232](https://github.com/cookiecutter/cookiecutter-django/pull/3232))
- Update pytest to 6.2.4 ([#3231](https://github.com/cookiecutter/cookiecutter-django/pull/3231))
- Update django-crispy-forms to 1.12.0 ([#3221](https://github.com/cookiecutter/cookiecutter-django/pull/3221))
- Update mypy to 0.902 ([#3219](https://github.com/cookiecutter/cookiecutter-django/pull/3219))
- Update django-coverage-plugin to 2.0.0 ([#3217](https://github.com/cookiecutter/cookiecutter-django/pull/3217))
- Update ipdb to 0.13.9 ([#3210](https://github.com/cookiecutter/cookiecutter-django/pull/3210))
- Update uvicorn to 0.14.0 ([#3207](https://github.com/cookiecutter/cookiecutter-django/pull/3207))
- Update pytest-cookies to 0.6.1 ([#3196](https://github.com/cookiecutter/cookiecutter-django/pull/3196))
- Update sphinx to 4.0.2 ([#3193](https://github.com/cookiecutter/cookiecutter-django/pull/3193))
- Update jinja2 to 3.0.1 ([#3189](https://github.com/cookiecutter/cookiecutter-django/pull/3189))

## [2021-06-19]
### Updated
- Update psycopg2 to 2.9.1 ([#3227](https://github.com/cookiecutter/cookiecutter-django/pull/3227))
- Update psycopg2-binary to 2.9.1 ([#3228](https://github.com/cookiecutter/cookiecutter-django/pull/3228))

## [2021-06-14]
### Changed
- Update black GitHub link in requirements ([#3222](https://github.com/cookiecutter/cookiecutter-django/pull/3222))

## [2021-06-09]
### Changed
- Fix link format in developing-locally.rst ([#3214](https://github.com/cookiecutter/cookiecutter-django/pull/3214))
### Updated
- Update pre-commit to 2.13.0 ([#3195](https://github.com/cookiecutter/cookiecutter-django/pull/3195))
- Update pytest-django to 4.4.0 ([#3212](https://github.com/cookiecutter/cookiecutter-django/pull/3212))
- Update mypy to 0.901 ([#3215](https://github.com/cookiecutter/cookiecutter-django/pull/3215))
- Auto-update pre-commit hooks ([#3206](https://github.com/cookiecutter/cookiecutter-django/pull/3206))
- Update black to 21.5b2 ([#3204](https://github.com/cookiecutter/cookiecutter-django/pull/3204))

## [2021-06-06]
### Changed
- Updated .pre-commit-config.yaml to self-update its dependencies ([#3208](https://github.com/cookiecutter/cookiecutter-django/pull/3208))

## [2021-06-05]
### Changed
- Shorthand for the officially supported buildpack ([#3211](https://github.com/cookiecutter/cookiecutter-django/pull/3211))

## [2021-06-02]
### Updated
- Update django to 3.1.12 ([#3209](https://github.com/cookiecutter/cookiecutter-django/pull/3209))

## [2021-05-18]
### Changed
- Move ARG PYTHON_VERSION=3.9-slim-buster to the global scope ([#3188](https://github.com/cookiecutter/cookiecutter-django/pull/3188))

## [2021-05-17]
### Updated
- Bump tiangolo/issue-manager from 0.3.0 to 0.4.0 ([#3186](https://github.com/cookiecutter/cookiecutter-django/pull/3186))
- Auto-update pre-commit hooks ([#3185](https://github.com/cookiecutter/cookiecutter-django/pull/3185))

## [2021-05-15]
### Changed
- Update watchgod to 0.7 ([#3177](https://github.com/cookiecutter/cookiecutter-django/pull/3177))
### Updated
- Auto-update pre-commit hooks ([#3184](https://github.com/cookiecutter/cookiecutter-django/pull/3184))
- Update black to 21.5b1 ([#3167](https://github.com/cookiecutter/cookiecutter-django/pull/3167))
- Update flake8 to 3.9.2 ([#3164](https://github.com/cookiecutter/cookiecutter-django/pull/3164))
- Update pytest-django to 4.3.0 ([#3182](https://github.com/cookiecutter/cookiecutter-django/pull/3182))
- Auto-update pre-commit hooks ([#3157](https://github.com/cookiecutter/cookiecutter-django/pull/3157))
- Update python-slugify to 5.0.2 ([#3161](https://github.com/cookiecutter/cookiecutter-django/pull/3161))
- Bump stefanzweifel/git-auto-commit-action from 4.10.0 to 4.11.0 ([#3171](https://github.com/cookiecutter/cookiecutter-django/pull/3171))
- Update sentry-sdk to 1.1.0 ([#3163](https://github.com/cookiecutter/cookiecutter-django/pull/3163))
- Bump actions/setup-python from 2 to 2.2.2 ([#3173](https://github.com/cookiecutter/cookiecutter-django/pull/3173))
- Update tox to 3.23.1 ([#3160](https://github.com/cookiecutter/cookiecutter-django/pull/3160))
- Update pytest to 6.2.4 ([#3156](https://github.com/cookiecutter/cookiecutter-django/pull/3156))
- Bump peter-evans/create-pull-request from 3.8.2 to 3.9.2 ([#3179](https://github.com/cookiecutter/cookiecutter-django/pull/3179))
- Update sphinx to 4.0.1 ([#3169](https://github.com/cookiecutter/cookiecutter-django/pull/3169))
- Update cookiecutter to 1.7.3 ([#3180](https://github.com/cookiecutter/cookiecutter-django/pull/3180))
- Update django to 3.1.11 ([#3178](https://github.com/cookiecutter/cookiecutter-django/pull/3178))

## [2021-05-06]
### Updated
- Update django to 3.1.10 ([#3162](https://github.com/cookiecutter/cookiecutter-django/pull/3162))

## [2021-05-04]
### Updated
- Update django to 3.1.9 ([#3155](https://github.com/cookiecutter/cookiecutter-django/pull/3155))

## [2021-04-30]
### Fixed
- Fix linting error in production.py ([#3148](https://github.com/cookiecutter/cookiecutter-django/pull/3148))

## [2021-04-29]
### Updated
- Update black to 21.4b2 ([#3147](https://github.com/cookiecutter/cookiecutter-django/pull/3147))
- Auto-update pre-commit hooks ([#3146](https://github.com/cookiecutter/cookiecutter-django/pull/3146))

## [2021-04-28]
### Changed
- Fix README link ([#3144](https://github.com/cookiecutter/cookiecutter-django/pull/3144))
### Updated
- Auto-update pre-commit hooks ([#3145](https://github.com/cookiecutter/cookiecutter-django/pull/3145))

## [2021-04-27]
### Updated
- Update pygithub to 1.55 ([#3141](https://github.com/cookiecutter/cookiecutter-django/pull/3141))
- Update black to 21.4b1 ([#3143](https://github.com/cookiecutter/cookiecutter-django/pull/3143))

## [2021-04-26]
### Updated
- Update black to 21.4b0 ([#3138](https://github.com/cookiecutter/cookiecutter-django/pull/3138))
- Auto-update pre-commit hooks ([#3137](https://github.com/cookiecutter/cookiecutter-django/pull/3137))

## [2021-04-21]
### Updated
- Auto-update pre-commit hooks ([#3133](https://github.com/cookiecutter/cookiecutter-django/pull/3133))
- Update django-extensions to 3.1.3 ([#3136](https://github.com/cookiecutter/cookiecutter-django/pull/3136))
- Update django-compressor to 2.4.1 ([#3135](https://github.com/cookiecutter/cookiecutter-django/pull/3135))
- Update pre-commit to 2.12.1 ([#3134](https://github.com/cookiecutter/cookiecutter-django/pull/3134))
- Update flake8 to 3.9.1 ([#3131](https://github.com/cookiecutter/cookiecutter-django/pull/3131))
- Update django-stubs to 1.8.0 ([#3127](https://github.com/cookiecutter/cookiecutter-django/pull/3127))
- Update sphinx to 3.5.4 ([#3126](https://github.com/cookiecutter/cookiecutter-django/pull/3126))

## [2021-04-15]
### Updated
- Update django-debug-toolbar to 3.2.1 ([#3129](https://github.com/cookiecutter/cookiecutter-django/pull/3129))

## [2021-04-14]
### Updated
- Bump stefanzweifel/git-auto-commit-action from v4.9.2 to v4.10.0 ([#3128](https://github.com/cookiecutter/cookiecutter-django/pull/3128))

## [2021-04-11]
### Updated
- Update pytest-django to 4.2.0 ([#3125](https://github.com/cookiecutter/cookiecutter-django/pull/3125))
- Update pylint-django to 2.4.3 ([#3122](https://github.com/cookiecutter/cookiecutter-django/pull/3122))

## [2021-04-09]
### Changed
- Update from Python 3.8 to Python 3.9 ([#3023](https://github.com/cookiecutter/cookiecutter-django/pull/3023))

## [2021-04-08]
### Changed
- Switch .dockerignore to explicit list ([#3121](https://github.com/cookiecutter/cookiecutter-django/pull/3121))
- Change Docker image to multi-stage build for Django ([#2815](https://github.com/cookiecutter/cookiecutter-django/pull/2815))
- Fix deprecated warning in middleware tests ([#3038](https://github.com/cookiecutter/cookiecutter-django/pull/3038))
### Updated
- Update pre-commit to 2.12.0 ([#3120](https://github.com/cookiecutter/cookiecutter-django/pull/3120))

## [2021-04-07]
### Changed
- Update django to 3.1.8 ([#3117](https://github.com/cookiecutter/cookiecutter-django/pull/3117))
### Fixed
- Fix linting via pre-commit on Github CI ([#3077](https://github.com/cookiecutter/cookiecutter-django/pull/3077))
- Fix gitlab-ci using duplicate key name for image ([#3112](https://github.com/cookiecutter/cookiecutter-django/pull/3112))
### Updated
- Update sentry-sdk to 1.0.0 ([#3080](https://github.com/cookiecutter/cookiecutter-django/pull/3080))
- Update gunicorn to 20.1.0 ([#3108](https://github.com/cookiecutter/cookiecutter-django/pull/3108))
- Update pre-commit to 2.12.0 ([#3118](https://github.com/cookiecutter/cookiecutter-django/pull/3118))
- Update django-extensions to 3.1.2 ([#3116](https://github.com/cookiecutter/cookiecutter-django/pull/3116))
- Update pillow to 8.2.0 ([#3113](https://github.com/cookiecutter/cookiecutter-django/pull/3113))
- Update pytest to 6.2.3 ([#3115](https://github.com/cookiecutter/cookiecutter-django/pull/3115))

## [2021-03-26]
### Updated
- Update djangorestframework to 3.12.4 ([#3107](https://github.com/cookiecutter/cookiecutter-django/pull/3107))

## [2021-03-25]
### Updated
- Update djangorestframework to 3.12.3 ([#3105](https://github.com/cookiecutter/cookiecutter-django/pull/3105))

## [2021-03-22]
### Updated
- Update django-crispy-forms to 1.11.2 ([#3104](https://github.com/cookiecutter/cookiecutter-django/pull/3104))
- Update sphinx to 3.5.3 ([#3103](https://github.com/cookiecutter/cookiecutter-django/pull/3103))
- Update ipdb to 0.13.7 ([#3102](https://github.com/cookiecutter/cookiecutter-django/pull/3102))
- Update sphinx-autobuild to 2021.3.14 ([#3101](https://github.com/cookiecutter/cookiecutter-django/pull/3101))
- Update isort to 5.8.0 ([#3100](https://github.com/cookiecutter/cookiecutter-django/pull/3100))
- Update pre-commit to 2.11.1 ([#3089](https://github.com/cookiecutter/cookiecutter-django/pull/3089))
- Update flake8 to 3.9.0 ([#3096](https://github.com/cookiecutter/cookiecutter-django/pull/3096))
- Update pillow to 8.1.2 ([#3084](https://github.com/cookiecutter/cookiecutter-django/pull/3084))
- Auto-update pre-commit hooks ([#3095](https://github.com/cookiecutter/cookiecutter-django/pull/3095))

## [2021-03-05]
### Changed
- Updated test_urls.py and views.py to re-use User.get_absolute_url() ([#3070](https://github.com/cookiecutter/cookiecutter-django/pull/3070))
### Updated
- Bump stefanzweifel/git-auto-commit-action from v4.9.1 to v4.9.2 ([#3082](https://github.com/cookiecutter/cookiecutter-django/pull/3082))

## [2021-03-03]
### Updated
- Update tox to 3.23.0 ([#3079](https://github.com/cookiecutter/cookiecutter-django/pull/3079))
- Update ipdb to 0.13.5 ([#3078](https://github.com/cookiecutter/cookiecutter-django/pull/3078))

## [2021-03-02]
### Fixed
- Fixes for pytest job in Github CI workflow ([#3076](https://github.com/cookiecutter/cookiecutter-django/pull/3076))
### Updated
- Update pillow to 8.1.1 ([#3075](https://github.com/cookiecutter/cookiecutter-django/pull/3075))
- Update coverage to 5.5 ([#3074](https://github.com/cookiecutter/cookiecutter-django/pull/3074))

## [2021-02-24]
### Updated
- Bump stefanzweifel/git-auto-commit-action from v4.9.0 to v4.9.1 ([#3069](https://github.com/cookiecutter/cookiecutter-django/pull/3069))

## [2021-02-23]
### Changed
- Update to Django 3.1 ([#3043](https://github.com/cookiecutter/cookiecutter-django/pull/3043))
- Lint with pre-commit on CI with Github actions ([#3066](https://github.com/cookiecutter/cookiecutter-django/pull/3066))
- Use exception var in status code pages if available ([#2992](https://github.com/cookiecutter/cookiecutter-django/pull/2992))

## [2021-02-22]
### Changed
- refactor: remove default cache settings in test.py ([#3064](https://github.com/cookiecutter/cookiecutter-django/pull/3064))
- Update django to 3.0.13 ([#3060](https://github.com/cookiecutter/cookiecutter-django/pull/3060))
### Fixed
- Fix missing Django Debug toolbar with node container ([#2865](https://github.com/cookiecutter/cookiecutter-django/pull/2865))
- Remove Email from User API ([#3055](https://github.com/cookiecutter/cookiecutter-django/pull/3055))
### Updated
- Bump stefanzweifel/git-auto-commit-action from v4.8.0 to v4.9.0 ([#3065](https://github.com/cookiecutter/cookiecutter-django/pull/3065))
- Update django-crispy-forms to 1.11.1 ([#3063](https://github.com/cookiecutter/cookiecutter-django/pull/3063))
- Update uvicorn to 0.13.4 ([#3062](https://github.com/cookiecutter/cookiecutter-django/pull/3062))
- Update mypy to 0.812 ([#3061](https://github.com/cookiecutter/cookiecutter-django/pull/3061))
- Update sentry-sdk to 0.20.3 ([#3059](https://github.com/cookiecutter/cookiecutter-django/pull/3059))
- Update tox to 3.22.0 ([#3057](https://github.com/cookiecutter/cookiecutter-django/pull/3057))
- Update sphinx to 3.5.1 ([#3056](https://github.com/cookiecutter/cookiecutter-django/pull/3056))

## [2021-02-16]
### Updated
- Update sentry-sdk to 0.20.2 ([#3054](https://github.com/cookiecutter/cookiecutter-django/pull/3054))
- Update sphinx to 3.5.0 ([#3053](https://github.com/cookiecutter/cookiecutter-django/pull/3053))

## [2021-02-13]
### Updated
- Update sentry-sdk to 0.20.1 ([#3052](https://github.com/cookiecutter/cookiecutter-django/pull/3052))

## [2021-02-12]
### Updated
- Update pre-commit to 2.10.1 ([#3045](https://github.com/cookiecutter/cookiecutter-django/pull/3045))
- Update sentry-sdk to 0.20.0 ([#3051](https://github.com/cookiecutter/cookiecutter-django/pull/3051))

## [2021-02-10]
### Updated
- Bump peter-evans/create-pull-request from v3.8.1 to v3.8.2 ([#3049](https://github.com/cookiecutter/cookiecutter-django/pull/3049))

## [2021-02-08]
### Updated
- Update django-extensions to 3.1.1 ([#3047](https://github.com/cookiecutter/cookiecutter-django/pull/3047))
- Bump peter-evans/create-pull-request from v3.8.0 to v3.8.1 ([#3046](https://github.com/cookiecutter/cookiecutter-django/pull/3046))

## [2021-02-06]
### Changed
- Removed Redundant test_case_sensitivity() and made test_not_authenticated() get the LOGIN_URL dynamically. ([#3041](https://github.com/cookiecutter/cookiecutter-django/pull/3041))
- Refactored users.forms to make the code more readeable ([#3029](https://github.com/cookiecutter/cookiecutter-django/pull/3029))
- Update django to 3.0.12 ([#3037](https://github.com/cookiecutter/cookiecutter-django/pull/3037))
### Updated
- Update tox to 3.21.4 ([#3044](https://github.com/cookiecutter/cookiecutter-django/pull/3044))

## [2021-02-01]
### Updated
- Update pytz to 2021.1 ([#3035](https://github.com/cookiecutter/cookiecutter-django/pull/3035))
- Update jinja2 to 2.11.3 ([#3033](https://github.com/cookiecutter/cookiecutter-django/pull/3033))
- Bump peter-evans/create-pull-request from v3.7.0 to v3.8.0 ([#3034](https://github.com/cookiecutter/cookiecutter-django/pull/3034))

## [2021-01-31]
### Changed
- Adding local celery instructions to developing-locally ([#3031](https://github.com/cookiecutter/cookiecutter-django/pull/3031))
### Updated
- Update django-crispy-forms to 1.11.0 ([#3032](https://github.com/cookiecutter/cookiecutter-django/pull/3032))

## [2021-01-28]
### Updated
- Update pre-commit to 2.10.0 ([#3028](https://github.com/cookiecutter/cookiecutter-django/pull/3028))
- Update django-anymail to 8.2 ([#3027](https://github.com/cookiecutter/cookiecutter-django/pull/3027))
- Update tox to 3.21.3 ([#3026](https://github.com/cookiecutter/cookiecutter-django/pull/3026))

## [2021-01-26]
### Changed
- Bump peter-evans/create-pull-request from v3.6.0 to v3.7.0 ([#3022](https://github.com/cookiecutter/cookiecutter-django/pull/3022))
- Using SuccessMessageMixin to send success message to django template ([#3021](https://github.com/cookiecutter/cookiecutter-django/pull/3021))
### Fixed
- Update admin to ignore *_name User attributes ([#3018](https://github.com/cookiecutter/cookiecutter-django/pull/3018))
### Updated
- Update coverage to 5.4 ([#3024](https://github.com/cookiecutter/cookiecutter-django/pull/3024))
- Update pytest to 6.2.2 ([#3020](https://github.com/cookiecutter/cookiecutter-django/pull/3020))
- Update django-cors-headers to 3.7.0 ([#3019](https://github.com/cookiecutter/cookiecutter-django/pull/3019))

## [2021-01-24]
### Changed
- Use defer for script tags (Fix #2922) ([#2927](https://github.com/cookiecutter/cookiecutter-django/pull/2927))
- Made Traefik conf much easier to understand and improved redirect res… ([#2838](https://github.com/cookiecutter/cookiecutter-django/pull/2838))
- Sentry Redis integration enabled by default in production. ([#2989](https://github.com/cookiecutter/cookiecutter-django/pull/2989))
- Add test for UserUpdateView.form_valid() ([#2949](https://github.com/cookiecutter/cookiecutter-django/pull/2949))
### Fixed
- Omit first_name and last_name in User model ([#2998](https://github.com/cookiecutter/cookiecutter-django/pull/2998))
### Updated
- Update django-celery-beat to 2.2.0 ([#3009](https://github.com/cookiecutter/cookiecutter-django/pull/3009))
- Update pyyaml to 5.4.1 ([#3011](https://github.com/cookiecutter/cookiecutter-django/pull/3011))
- Update mypy to 0.800 ([#3013](https://github.com/cookiecutter/cookiecutter-django/pull/3013))
- Update factory-boy to 3.2.0 ([#2986](https://github.com/cookiecutter/cookiecutter-django/pull/2986))
- Update tox to 3.21.2 ([#3010](https://github.com/cookiecutter/cookiecutter-django/pull/3010))

## [2021-01-22]
### Changed
- Use self.request.user instead of second query ([#3012](https://github.com/cookiecutter/cookiecutter-django/pull/3012))

## [2021-01-14]
### Updated
- Update tox to 3.21.1 ([#3006](https://github.com/cookiecutter/cookiecutter-django/pull/3006))

## [2021-01-10]
### Updated
- Update pylint-django to 2.4.2 ([#3003](https://github.com/cookiecutter/cookiecutter-django/pull/3003))
- Update tox to 3.21.0 ([#3002](https://github.com/cookiecutter/cookiecutter-django/pull/3002))

## [2021-01-08]
### Changed
- Upgrade Travis to Focal ([#2999](https://github.com/cookiecutter/cookiecutter-django/pull/2999))
### Updated
- Update pylint-django to 2.4.1 ([#3001](https://github.com/cookiecutter/cookiecutter-django/pull/3001))
- Update sphinx to 3.4.3 ([#3000](https://github.com/cookiecutter/cookiecutter-django/pull/3000))
- Update pylint-django to 2.4.0 ([#2996](https://github.com/cookiecutter/cookiecutter-django/pull/2996))

## [2021-01-04]
### Updated
- Update isort to 5.7.0 ([#2988](https://github.com/cookiecutter/cookiecutter-django/pull/2988))
- Update uvicorn to 0.13.3 ([#2987](https://github.com/cookiecutter/cookiecutter-django/pull/2987))
- Auto-update pre-commit hooks ([#2990](https://github.com/cookiecutter/cookiecutter-django/pull/2990))
- Update sphinx to 3.4.2 ([#2995](https://github.com/cookiecutter/cookiecutter-django/pull/2995))
- Update pillow to 8.1.0 ([#2993](https://github.com/cookiecutter/cookiecutter-django/pull/2993))

## [2020-12-29]
### Updated
- Update pygithub to 1.54.1 ([#2982](https://github.com/cookiecutter/cookiecutter-django/pull/2982))
- Update django-storages to 1.11.1 ([#2981](https://github.com/cookiecutter/cookiecutter-django/pull/2981))

## [2020-12-26]
### Updated
- Update sphinx to 3.4.1 ([#2985](https://github.com/cookiecutter/cookiecutter-django/pull/2985))
- Update pytz to 2020.5 ([#2984](https://github.com/cookiecutter/cookiecutter-django/pull/2984))

## [2020-12-23]
### Changed
- Bump peter-evans/create-pull-request from v3.5.2 to v3.6.0 ([#2980](https://github.com/cookiecutter/cookiecutter-django/pull/2980))
### Updated
- Update flower to 0.9.7 ([#2979](https://github.com/cookiecutter/cookiecutter-django/pull/2979))
- Update sphinx to 3.4.0 ([#2978](https://github.com/cookiecutter/cookiecutter-django/pull/2978))
- Update coverage to 5.3.1 ([#2977](https://github.com/cookiecutter/cookiecutter-django/pull/2977))
- Update uvicorn to 0.13.2 ([#2976](https://github.com/cookiecutter/cookiecutter-django/pull/2976))

## [2020-12-18]
### Changed
- Bump stefanzweifel/git-auto-commit-action from v4.7.2 to v4.8.0 ([#2972](https://github.com/cookiecutter/cookiecutter-django/pull/2972))
### Updated
- Update django-storages to 1.11 ([#2973](https://github.com/cookiecutter/cookiecutter-django/pull/2973))
- Update pytest to 6.2.1 ([#2971](https://github.com/cookiecutter/cookiecutter-django/pull/2971))
- Auto-update pre-commit hooks ([#2970](https://github.com/cookiecutter/cookiecutter-django/pull/2970))

## [2020-12-14]
### Updated
- Update pytest to 6.2.0 ([#2968](https://github.com/cookiecutter/cookiecutter-django/pull/2968))
- Update django-cors-headers to 3.6.0 ([#2967](https://github.com/cookiecutter/cookiecutter-django/pull/2967))
- Update uvicorn to 0.13.1 ([#2966](https://github.com/cookiecutter/cookiecutter-django/pull/2966))

## [2020-12-10]
### Changed
- Hot-reload support to celery ([#2554](https://github.com/cookiecutter/cookiecutter-django/pull/2554))
### Updated
- Update uvicorn to 0.13.0 ([#2962](https://github.com/cookiecutter/cookiecutter-django/pull/2962))
- Update sentry-sdk to 0.19.5 ([#2965](https://github.com/cookiecutter/cookiecutter-django/pull/2965))

## [2020-12-09]
### Changed
- Bump peter-evans/create-pull-request from v3.5.1 to v3.5.2 ([#2964](https://github.com/cookiecutter/cookiecutter-django/pull/2964))

## [2020-12-08]
### Updated
- Update pre-commit to 2.9.3 ([#2961](https://github.com/cookiecutter/cookiecutter-django/pull/2961))

## [2020-12-04]
### Updated
- Update django-debug-toolbar to 3.2 ([#2959](https://github.com/cookiecutter/cookiecutter-django/pull/2959))

## [2020-12-02]
### Updated
- Update django-model-utils to 4.1.1 ([#2957](https://github.com/cookiecutter/cookiecutter-django/pull/2957))
- Update pygithub to 1.54 ([#2958](https://github.com/cookiecutter/cookiecutter-django/pull/2958))

## [2020-11-26]
### Updated
- Update django-extensions to 3.1.0 ([#2947](https://github.com/cookiecutter/cookiecutter-django/pull/2947))
- Update pre-commit to 2.9.2 ([#2948](https://github.com/cookiecutter/cookiecutter-django/pull/2948))
- Update django-allauth to 0.44.0 ([#2945](https://github.com/cookiecutter/cookiecutter-django/pull/2945))

## [2020-11-25]
### Changed
- Bump peter-evans/create-pull-request from v3.5.0 to v3.5.1 ([#2944](https://github.com/cookiecutter/cookiecutter-django/pull/2944))

## [2020-11-23]
### Updated
- Update uvicorn to 0.12.3 ([#2943](https://github.com/cookiecutter/cookiecutter-django/pull/2943))
- Update pre-commit to 2.9.0 ([#2942](https://github.com/cookiecutter/cookiecutter-django/pull/2942))

## [2020-11-21]
### Changed
- Fix after uvicorn 0.12.0 - Ship extra dependencies ([#2939](https://github.com/cookiecutter/cookiecutter-django/pull/2939))

## [2020-11-20]
### Updated
- Update sentry-sdk to 0.19.4 ([#2938](https://github.com/cookiecutter/cookiecutter-django/pull/2938))

## [2020-11-19]
### Updated
- Update django-crispy-forms to 1.10.0 ([#2937](https://github.com/cookiecutter/cookiecutter-django/pull/2937))

## [2020-11-17]
### Changed
- Bump peter-evans/create-pull-request from v2 to v3.5.0 ([#2936](https://github.com/cookiecutter/cookiecutter-django/pull/2936))

## [2020-11-15]
### Changed
- Fix formatting in docs ([#2935](https://github.com/cookiecutter/cookiecutter-django/pull/2935))

## [2020-11-13]
### Changed
- Upgrade factory-boy to 3.1.0 ([#2932](https://github.com/cookiecutter/cookiecutter-django/pull/2932))
### Updated
- Update sentry-sdk to 0.19.3 ([#2933](https://github.com/cookiecutter/cookiecutter-django/pull/2933))
- Update sphinx to 3.3.1 ([#2934](https://github.com/cookiecutter/cookiecutter-django/pull/2934))

## [2020-11-12]
### Changed
- Migrate CI to Github Actions ([#2931](https://github.com/cookiecutter/cookiecutter-django/pull/2931))

## [2020-11-06]
### Updated
- Update djangorestframework to 3.12.2 ([#2930](https://github.com/cookiecutter/cookiecutter-django/pull/2930))

## [2020-11-04]
### Changed
- Fix docs service and add RTD support ([#2920](https://github.com/cookiecutter/cookiecutter-django/pull/2920))
- Bump stefanzweifel/git-auto-commit-action from v4.6.0 to v4.7.2 ([#2914](https://github.com/cookiecutter/cookiecutter-django/pull/2914))
### Updated
- Auto-update pre-commit hooks ([#2908](https://github.com/cookiecutter/cookiecutter-django/pull/2908))
- Update mypy to 0.790 ([#2886](https://github.com/cookiecutter/cookiecutter-django/pull/2886))
- Update django-stubs to 1.7.0 ([#2916](https://github.com/cookiecutter/cookiecutter-django/pull/2916))

## [2020-11-03]
### Updated
- Update sentry-sdk to 0.19.2 ([#2926](https://github.com/cookiecutter/cookiecutter-django/pull/2926))
- Update sphinx to 3.3.0 ([#2925](https://github.com/cookiecutter/cookiecutter-django/pull/2925))
- Update django to 3.0.11 ([#2924](https://github.com/cookiecutter/cookiecutter-django/pull/2924))
- Update pytz to 2020.4 ([#2923](https://github.com/cookiecutter/cookiecutter-django/pull/2923))
- Update pre-commit to 2.8.2 ([#2919](https://github.com/cookiecutter/cookiecutter-django/pull/2919))
- Update pytest to 6.1.2 ([#2917](https://github.com/cookiecutter/cookiecutter-django/pull/2917))
- Update sh to 1.14.1 ([#2912](https://github.com/cookiecutter/cookiecutter-django/pull/2912))
- Update pytest-django to 4.1.0 ([#2911](https://github.com/cookiecutter/cookiecutter-django/pull/2911))
- Update pillow to 8.0.1 ([#2910](https://github.com/cookiecutter/cookiecutter-django/pull/2910))
- Update django-celery-beat to 2.1.0 ([#2907](https://github.com/cookiecutter/cookiecutter-django/pull/2907))
- Update uvicorn to 0.12.2 ([#2906](https://github.com/cookiecutter/cookiecutter-django/pull/2906))

## [2020-10-19]
### Updated
- Update sentry-sdk to 0.19.1 ([#2905](https://github.com/cookiecutter/cookiecutter-django/pull/2905))

## [2020-10-17]
### Updated
- Update django-allauth to 0.43.0 ([#2901](https://github.com/cookiecutter/cookiecutter-django/pull/2901))
- Update pytest-django to 4.0.0 ([#2903](https://github.com/cookiecutter/cookiecutter-django/pull/2903))

## [2020-10-15]
### Updated
- Update pillow to 8.0.0 ([#2898](https://github.com/cookiecutter/cookiecutter-django/pull/2898))

## [2020-10-14]
### Updated
- Auto-update pre-commit hooks ([#2897](https://github.com/cookiecutter/cookiecutter-django/pull/2897))
- Update sentry-sdk to 0.19.0 ([#2896](https://github.com/cookiecutter/cookiecutter-django/pull/2896))

## [2020-10-13]
### Updated
- Update isort to 5.6.4 ([#2895](https://github.com/cookiecutter/cookiecutter-django/pull/2895))

## [2020-10-12]
### Changed
- Bump stefanzweifel/git-auto-commit-action from v4.5.1 to v4.6.0 ([#2893](https://github.com/cookiecutter/cookiecutter-django/pull/2893))
### Updated
- Auto-update pre-commit hooks ([#2892](https://github.com/cookiecutter/cookiecutter-django/pull/2892))

## [2020-10-11]
### Updated
- Auto-update pre-commit hooks ([#2890](https://github.com/cookiecutter/cookiecutter-django/pull/2890))
- Update isort to 5.6.3 ([#2891](https://github.com/cookiecutter/cookiecutter-django/pull/2891))
- Update django-anymail to 8.1 ([#2887](https://github.com/cookiecutter/cookiecutter-django/pull/2887))
- Update tox to 3.20.1 ([#2885](https://github.com/cookiecutter/cookiecutter-django/pull/2885))

## [2020-10-09]
### Updated
- Auto-update pre-commit hooks ([#2884](https://github.com/cookiecutter/cookiecutter-django/pull/2884))
- Update isort to 5.6.1 ([#2883](https://github.com/cookiecutter/cookiecutter-django/pull/2883))

## [2020-10-08]
### Changed
- Add dedicated websockets package ([#2881](https://github.com/cookiecutter/cookiecutter-django/pull/2881))
### Updated
- Update isort to 5.6.0 ([#2882](https://github.com/cookiecutter/cookiecutter-django/pull/2882))

## [2020-10-04]
### Updated
- Update pytest to 6.1.1 ([#2880](https://github.com/cookiecutter/cookiecutter-django/pull/2880))
- Update mypy and django-stubs ([#2874](https://github.com/cookiecutter/cookiecutter-django/pull/2874))
- Auto-update pre-commit hooks ([#2876](https://github.com/cookiecutter/cookiecutter-django/pull/2876))
- Update flake8 to 3.8.4 ([#2877](https://github.com/cookiecutter/cookiecutter-django/pull/2877))

## [2020-10-01]
### Changed
- Bump actions/setup-python from v2.1.2 to v2.1.3 ([#2869](https://github.com/cookiecutter/cookiecutter-django/pull/2869))
### Updated
- Update ipdb to 0.13.4 ([#2873](https://github.com/cookiecutter/cookiecutter-django/pull/2873))
- Auto-update pre-commit hooks ([#2867](https://github.com/cookiecutter/cookiecutter-django/pull/2867))
- Update uvicorn to 0.12.1 ([#2866](https://github.com/cookiecutter/cookiecutter-django/pull/2866))
- Update isort to 5.5.4 ([#2864](https://github.com/cookiecutter/cookiecutter-django/pull/2864))
- Update sentry-sdk to 0.18.0 ([#2863](https://github.com/cookiecutter/cookiecutter-django/pull/2863))
- Update djangorestframework to 3.12.1 ([#2862](https://github.com/cookiecutter/cookiecutter-django/pull/2862))
- Update pytest to 6.1.0 ([#2859](https://github.com/cookiecutter/cookiecutter-django/pull/2859))
- Update django-debug-toolbar to 3.1.1 ([#2855](https://github.com/cookiecutter/cookiecutter-django/pull/2855))

## [2020-09-23]
### Updated
- Update sentry-sdk to 0.17.7 ([#2847](https://github.com/cookiecutter/cookiecutter-django/pull/2847))
- Update django-debug-toolbar to 3.1 ([#2846](https://github.com/cookiecutter/cookiecutter-django/pull/2846))

## [2020-09-21]
### Changed
- Adding GitHub-Action CI Option ([#2837](https://github.com/cookiecutter/cookiecutter-django/pull/2837))
### Updated
- Update django-debug-toolbar to 3.0 ([#2842](https://github.com/cookiecutter/cookiecutter-django/pull/2842))
- Auto-update pre-commit hooks ([#2843](https://github.com/cookiecutter/cookiecutter-django/pull/2843))
- Update isort to 5.5.3 ([#2844](https://github.com/cookiecutter/cookiecutter-django/pull/2844))

## [2020-09-18]
### Updated
- Update django-extensions to 3.0.9 ([#2839](https://github.com/cookiecutter/cookiecutter-django/pull/2839))

## [2020-09-16]
### Updated
- Update sentry-sdk to 0.17.6 ([#2833](https://github.com/cookiecutter/cookiecutter-django/pull/2833))
- Update pytest-django to 3.10.0 ([#2832](https://github.com/cookiecutter/cookiecutter-django/pull/2832))

## [2020-09-14]
### Fixed
- Downgrade Celery to 4.4.6 ([#2829](https://github.com/cookiecutter/cookiecutter-django/pull/2829))
### Updated
- Update sentry-sdk to 0.17.5 ([#2828](https://github.com/cookiecutter/cookiecutter-django/pull/2828))
- Update coverage to 5.3 ([#2826](https://github.com/cookiecutter/cookiecutter-django/pull/2826))
- Update django-storages to 1.10.1 ([#2825](https://github.com/cookiecutter/cookiecutter-django/pull/2825))

## [2020-09-12]
### Updated
- Updating Traefik version from 2.0 to 2.2.11 ([#2814](https://github.com/cookiecutter/cookiecutter-django/pull/2814))
- Update pytest to 6.0.2 ([#2819](https://github.com/cookiecutter/cookiecutter-django/pull/2819))
- Update django-anymail to 8.0 ([#2818](https://github.com/cookiecutter/cookiecutter-django/pull/2818))

## [2020-09-11]
### Updated
- Auto-update pre-commit hooks ([#2809](https://github.com/cookiecutter/cookiecutter-django/pull/2809))

## [2020-09-10]
### Updated
- Update isort to 5.5.2 ([#2807](https://github.com/cookiecutter/cookiecutter-django/pull/2807))
- Update sentry-sdk to 0.17.4 ([#2805](https://github.com/cookiecutter/cookiecutter-django/pull/2805))

## [2020-09-09]
### Changed
- Update actions/setup-python requirement to v2.1.2 ([#2804](https://github.com/cookiecutter/cookiecutter-django/pull/2804))
- Clean up nested venv files from `.gitignore` ([#2800](https://github.com/cookiecutter/cookiecutter-django/pull/2800))

## [2020-09-08]
### Changed
- Traeffik and Django dockerfile changes ([#2801](https://github.com/cookiecutter/cookiecutter-django/pull/2801))

## [2020-09-07]
### Changed
- Add :z/:Z to mounted volumes in {local,production}.yml ([#2663](https://github.com/cookiecutter/cookiecutter-django/pull/2663))
- Remove --no-binary option for psycopg2 ([#2798](https://github.com/cookiecutter/cookiecutter-django/pull/2798))
- Updated Gitlab CI to use Python 3.8 instead of Python 3.7 ([#2794](https://github.com/cookiecutter/cookiecutter-django/pull/2794))
### Fixed
- Fix options for sphinx-autobuild in docs Makefile ([#2799](https://github.com/cookiecutter/cookiecutter-django/pull/2799))
### Updated
- Update psycopg2-binary to 2.8.6 ([#2797](https://github.com/cookiecutter/cookiecutter-django/pull/2797))

## [2020-09-05]
### Updated
- Auto-update pre-commit hooks ([#2793](https://github.com/cookiecutter/cookiecutter-django/pull/2793))

## [2020-09-04]
### Updated
- Update django-extensions to 3.0.8 ([#2792](https://github.com/cookiecutter/cookiecutter-django/pull/2792))
- Update isort to 5.5.1 ([#2791](https://github.com/cookiecutter/cookiecutter-django/pull/2791))
- Auto-update pre-commit hooks ([#2790](https://github.com/cookiecutter/cookiecutter-django/pull/2790))
- Update isort to 5.5.0 ([#2789](https://github.com/cookiecutter/cookiecutter-django/pull/2789))

## [2020-09-02]
### Changed
- Add environment and traces_sample_rate keyword to sentry_sdk.init ([#2777](https://github.com/cookiecutter/cookiecutter-django/pull/2777))
### Updated
- Update sentry-sdk to 0.17.3 ([#2788](https://github.com/cookiecutter/cookiecutter-django/pull/2788))
- Update django-extensions to 3.0.7 ([#2787](https://github.com/cookiecutter/cookiecutter-django/pull/2787))

## [2020-09-01]
### Changed
- Exclude venv directory and update document link ([#2780](https://github.com/cookiecutter/cookiecutter-django/pull/2780))
### Updated
- Update tox to 3.20.0 ([#2786](https://github.com/cookiecutter/cookiecutter-django/pull/2786))
- Update django-storages to 1.10 ([#2781](https://github.com/cookiecutter/cookiecutter-django/pull/2781))
- Update sentry-sdk to 0.17.2 ([#2784](https://github.com/cookiecutter/cookiecutter-django/pull/2784))
- Update django to 3.0.10 ([#2785](https://github.com/cookiecutter/cookiecutter-django/pull/2785))
- Update sphinx-autobuild to 2020.9.1 ([#2782](https://github.com/cookiecutter/cookiecutter-django/pull/2782))
- Update django-extensions to 3.0.6 ([#2783](https://github.com/cookiecutter/cookiecutter-django/pull/2783))

## [2020-08-31]
### Updated
- Update sh to 1.14.0 ([#2779](https://github.com/cookiecutter/cookiecutter-django/pull/2779))
- Update sentry-sdk to 0.17.1 ([#2778](https://github.com/cookiecutter/cookiecutter-django/pull/2778))

## [2020-04-13]
### Changed
- Updated to Python 3.8 (@codnee)
- Moved coverage config in setup.cfg (@danihodovic)

## [2020-04-08]
### Fixed
- Internal IPs for debug toolbar (@dudanogueira)

## [2020-04-04]
### Fixed
- Added compress command with Django compressor (@gwiskur)

## [2020-03-23]
### Changed
- Updated project to Django 3.0

## [2020-03-17]
### Changed
- Handle paths using Pathlib (@jules-ch)

### Fixed
- Pre-commit hook regex (@demestav)

## [2020-03-16]
### Added
- Support for all Anymail providers (@Andrew-Chen-Wang)
### Fixed
- Django compressor setup (@jameswilliams1)

## [2020-01-23]
### Changed
- Fix UserFactory to set the password if provided (@BoPeng)
- Update documentation files with latest Sphinx (@howiezhao)

## [2020-01-12]
### Changed
- Fix mypy setup and added django-stubs (@danifus)
- Add Gitlab CI as option (@ikhomutov)

## [2020-01-11]
### Changed
- Speed up & reduce size for production Django image (@maxp)
- Bumped runtime version for Heroku (@Isaac12x)
- Added Debian 10 (Buster) OS dependencies (@ddiazpinto)
- Update Traefik to v2 (@blaxpy)
- Switched Docker images from Alpine based to Debian based (@trungdong)

## [2019-10-06]
### Changed
- Default Python version is now 3.7 (@nicolas471)

## [2019-10-04]
### Fixed
- Fix static files handling on GCP (@caioariede)

## [2019-10-03]
### Fixed
- Fix incompatible combination between Whitenoise and no cloud provider (@caioariede)

## [2019-07-09]
### Fixed
- Always use test settings in pytest (@danihodovic)
- Remove gunicorn from `INSTALLED_APPS` (@danihodovic)
- Remove `EMAIL_HOST` and `EMAIL_PORT` with locmem backend (@danihodovic)

### Added
- Add `EMAIL_TIMEOUT` (@danihodovic)

## [2019-06-22]
### Fixed
- Remove redundant template debug setting (@danihodovic)

## [2019-06-19]
### Fixed
- Fix removal carriage returns in docker scripts (@timclaessens)

## [2019-06-15]
### Fixed
- Issue with Pycharm setup for running things in Docker compose (@foarsitter)

## [2019-06-06]
### Changed
- Update generated Travis config (@browniebroke)

## [2019-06-03]
### Added
- Installed `django-celery-beat` to keep scheduled tasks in DB (@keyvanm)

## [2019-05-28]
### Changed
- Use GCP acronym rather than inconsistent GCE/GCS (@tanoabeleyra)

## [2019-05-27]
### Changed
- Made cloud provider optional (@tanoabeleyra)
- Updated to Django 2.2.1 (@browniebroke)

### Fixed
- Celery worker-related setting names (@browniebroke)

## [2019-05-18]
### Removed
- Remove the user list view (@browniebroke)

### Fixed
- Static storage default ACL (@browniebroke)

## [2019-05-17]
### Fixed
- Added `LocaleMiddleware` to the list of middlewares (@tanoabeleyra)
- Added `LOCALE_PATH` to settings (@tanoabeleyra)

## [2019-05-16]
### Changed
- Users app to have a translated verbose name (@tanoabeleyra)
- Logging configuration for local (@browniebroke)

## [2019-05-08]
### Changed
- Upgraded to Django 2.1 (@browniebroke)

## [2019-04-07]
### Added
- Support for Google Cloud Storage (@ahhda)

## [2019-04-03]
### Added
- Command to backup Db to AWS S3 (@foarsitter)

## [2019-03-25]
### Added
- Node image to run Gulp with Docker (@browniebroke)

## [2019-03-19]
### Changed
- Replaced Caddy with Traefik (@demestav)

## [2019-03-11]
### Changed
- Sentry integration from Raven to Sentry-SDK (@gfabricio)
- Made Redis config conditional on Celery locally (@demestav)

## [2019-03-11]
### Added
- Automatic migrations on Heroku (@yunti)

## [2019-03-06]
### Fixed
- Missing script tag in Travis config (@btknu)

## [2019-03-02]
### Changed
- Celery eager setting in local setting with Docker (@keithjeb)

## [2019-03-01]
### Updated
- All NPM dependencies (@takkaria)

## [2018-11-13]
### Changed
- Security settings in Dev (@carlmjohnson)

## [2018-11-20]
### Fixed
- Passing the CSRF header from the reverse proxy to Django server for DRF (@hpbruna)

## [2018-11-12]
### Fixed
- Initialisation of Celery app (@glasslion)

## [2018-10-24]
### Fixed
- Persisting of iPython history between sessions (@davitovmasyan)

### Added
- Postgres 10.5 option (@jleclanche)

## [2018-09-18]
### Added
- Included `mypy` in dependencies and run it in tests (@apirobot)

## [2018-09-18]
### Fixed
- Avoid `$` in environment variables to workaround a bug from django-environ (@browniebroke)

## [2018-09-16]
### Fixed
- Bug in ordering of Middleware for production config (@ChrisPappalardo)

## [2018-09-12]
### Fixed
- URLs for Static and Media for S3 buckets in regions other than N. Virginia (@umrashrf)

## [2018-09-09]
### Changed
- Name of static and media storage classes (@sfdye)

## [2018-09-01]
### Changed
- Make static and media storage fully-fledged classes (@erfaan)

## [2018-08-28]
### Fixed
- Running tests in docker test script (@apirobot)

## [2018-07-23]
### Changed
- Test commands to use pytest (@jcass77)

### Removed
- Some hacks leftovers from Bootstrap v4 beta in `project.js` (@hendrikschneider)

## [2018-07-12]
### Changed
- Upgraded to Bootstrap 4.1.1 (@mostaszewski)

## [2018-06-25]
### Added
- Flower integration with Docker (@webyneter)

## [2018-06-25]
### Changed
- Rewrite user app test to use a pytest style (@webyneter)

## [2018-06-21]
### Added
- Extend & update Celery config (@webyneter & @apirobot)

## [2018-05-25]
### Fixed
- Build issues due to incompatibility between libressl & openssl (@SassanoM)

## [2018-05-21]
### Changed
- Updated Caddy to 0.11 and pin its version (@webyneter)

## [2018-05-14]
### Changed
- Replace `awesome-slugify` by `python-slugify` (@hongquan)
- Migrate to Django 2.0+ URL style (@saschalalala)

## [2018-05-05]
### Fixed
- Postgres backup & restore commands (@webyneter)

## [2018-04-10]
### Changed
- Simplify configuration (@danidee10)

## [2018-04-08]
### Added
- Adopt Black code style (@pydanny)

## [2018-03-27]
### Fixed
- Simplified extra Celery config generated when opted out (@webyneter)

## [2018-03-21]
### Removed
- Remove Opbeat support (@sfdye)

## [2018-03-16]
### Fixed
- Install `psycopg2-binary` when using Docker locally (@browniebroke)

## [2018-03-14]
### Fixed
- Fixed and improved Postgres backup & restore scripts (@webyneter)

## [2018-03-10]
### Changed
- Simplify Mailgun setting (@browniebroke)

## [2018-03-06]
### Changed
- Convert string formatting to f-strings (@sfdye)

## [2018-03-01]
### Changed
- Celery to use JSON serialization by default (@adammsteele)
- Use Docker version from Travis to run tests (@browniebroke)

## [2018-02-16]
### Changed
- Upgraded to Django 2.0 (@epicwhale)

## [2018-01-15]
### Changed
- Removed Elastic Beanstalk support (@pydanny)

## [2017-12-28]
### Changed
- Upgraded to Django 1.11 (@pydanny)

## [2017-10-08]
### Changed
- Elastic Beanstalk: Added --noinput to migrate command (@MightySCollins )

## [2017-10-07]
### Added
- Finished first pass at Elastic Beanstalk docs (@pydanny & @audreyr)
### Deleted
- Removed Heroku instant deploy button (@pydanny)


##[2016-09-29]
### Added
- Added default `AUTH_PASSWORD_VALIDATORS` configuration, generated by django 1.10 startproject. See [Password Validation docs](https://docs.djangoproject.com/en/1.10/topics/auth/passwords/#module-django.contrib.auth.password_validation") (@luzfcb)
- Rename `MIDDLEWARE_CLASSES` to `MIDDLEWARE` to enable support to [new style middleware](https://github.com/django/deps/blob/master/final/0005-improved-middleware.rst) introduced in Django 1.10 (@luzfcb)
- New setting `MAILGUN_SENDER_DOMAIN` to allow sending mail from any domain other than those registered with mailgun (@jangeador)
- add `urlpatterns` configuration to django-debug-toolbar, because the automatic configuration of `urlpatterns` was removed from django-debug-toolbar (@luzfcb)
- Added Temporary workaround on `requirements/local.txt` to fix django-debug-toolbar issue: https://github.com/cookiecutter/cookiecutter-django/issues/827 (@luzfcb)

### Changed
- Upgrade to Django 1.10.1 (@luzfcb)
- Upgrade django-model-utils to 2.6, django-redis to 4.5.0, redis to 2.10.5, Sphinx to 1.4.6, pytest-django to 3.0.0, django-anymail to 0.5, raven to 5.27.1, whitenoise to 3.2.2 (@luzfcb)
- Upgrade to Bootstrap 4 Alpha 4, jQuery to 3.1.1, tether.js to 1.3.7 (@luzfcb)
- Update `manage.py` to use same code of `manage.py` from Django 1.10 (@luzfcb)
- Sync `sites` app migrations with django 1.10, and fix aditional migrations to `sites` and `user` app (@luzfcb)
d changed 'admin' url on `config/urls.py`, to stay the same as generated by django 1.10 (@luzfcb)
- Make test_docker.sh tests pass by passing new password auth rules (@ssteinerx)

### Removed
- Removed django-autoslug because not support django 1.10 at this date (@luzfcb)


##[2016-09-10]
### Changed
- Use app registry instead of INSTALLED_APPS to discover celery tasks (@dhepper)
- PEP8 imports fix (@aleprovencio)

### Removed
- Removed django-floppyforms (@pydanny)

##[2016-09-08]
### Removed
- Webpack support, see #774 (@ssteinerx)

##[2016-08-10]
## Added
- PostgreSQL versions are now selectable, instead of defaulting to 9.5; the minimum version is 9.2, which is supported by [Heroku](https://devcenter.heroku.com/articles/heroku-postgresql#version-support-and-legacy-infrastructure) and Django (@burhan)
- Fixed minor issue in the README.rst (@burhan)

##[2016-08-03]
## Changed
- Upgrade to Bootstrap 4 Alpha 3 and its dependencies, including jQuery (@audreyr)

##[2016-06-25]
## Changed
- use `https` instead `ssh` to clone [cookiecutter-webpack](https://github.com/hzdg/cookiecutter-webpack) if `Webpack` is selected as `JS Task Runner` - fix issue #647 (@luzfcb and @resakse)

##[2016-06-24]
## Added
- Settings file for running tests faster (@audreyr)
- Add GPLv3 licence support (@cgaspoz)

## Changed
- Makes the database backups compressed. restores compressed backups (@jangeador)
- Review and edit django-allauth templates (@kappataumu)

##[2016-06-19]
## Added
- Webpack as an option (@goldhand)

##[2016-06-17]
## Added
- django-compressor support (@andresgz)
- Debian Jessie OS Requirements (@ddiazpinto)

##[2016-06-14]
### Changed
- Move Docker backups to their own section (@pydanny)

##[2016-06-13]
### Changed
- Use latest redis image in Docker (@pydanny)
- Documentation cleanup and corrections (@audreyr)

##[2016-06-12]
### Changed
- Documentation cleanup and corrections (@kappataumu)

##[2016-06-11]
### Changed
- Enhancements to the developing locally docs (@antoniablair)

##[2016-06-06]
### Changed
- Pin Bootstrap CSS and JS to v4.0.0-alpha.2, use minified versions

##[2016-06-05]
### Added
- Configurable admin for users (@pydanny, @jayfk, @dezoito)

##[2016-06-04]
### Added
- Let's Encrypt automation and instruction (@mjsisley and @chrisdev)

##[2016-06-03]
### Added
- Documentation for debugging with Docker (@mjsisley)
- Apache 2 License option in `cookiecutter.json` (@dot2dotseurat)
- Removed unnecessary version check from `pre_gen_project.py` (@suledev)
- Add gulp alternative as a js task runner and fix navbar style issue (@viviangb and @xpostudio4)

### Deleted
- AngularJS (@pydanny)
- django-secure (@xpostudio4)

##[2016-06-02]
### Added
- Added better instructions for installing postgres on Mac OS X (@dot2dotseurat )

##[2016-05-22]
### Added
- Added instructions for copying backups from docker to host (@phiberjenz)
- Added mailhog docker container (@noisy)

##[2016-05-15]
### Added
- Added GitLab continuous integration article to README.rst (@dezoito)

## [2016-05-13]
### Changed
- Update version of pyflakes to 1.2.3, django-extensions to 1.6.7 and gunicorn to 19.5.0 (@luzfcb)
- Update version of AngularJS to 1.5.5 (@luzfcb)

### Removed
- Remove Raven 404 catch middleware. Fix #367 (@pydanny)

## [2016-05-09]
### Changed
- Improved mailhog usage documentation on `developing-locally.rst`  (@shireenrao)
- Replaced all `readthedocs.org` referencies to point to the new domain `readthedocs.io` (@luzfcb)
- Update version of pyflakes (@luzfcb)

## [2016-05-08]
### Changed
- Updated whitenoise configuration to match changes in version 3.0 (@trungdong)

## [2016-05-07]
### Added
- Added Ubuntu 16.04 dependencies on a new dependency file `requirements.apt.xenial` (@raonyguimaraes)

### Changed
- Small improvements in ``install_os_dependencies.sh`` support new dependency file (@raonyguimaraes)

## [2016-05-06]
### Changed
- Update version of pyflakes (@pydanny)

## [2016-05-03]
### Changed
- Update version of Django, django-extensions, django-mailgun (@luzfcb)

### [2016-05-01]
### Changed
- Restored the Pycharm project configuration files, that was accidentally removed in [15f350f](https://github.com/cookiecutter/cookiecutter-django/commit/15f350f05e2b49b4bdff0bdaa2b2ff260606e0f6) (@luzfcb @Newton715)

### [2016-04-30]
### Changed
- Small fixes to utility scripts (@scast)

### [2016-04-26]
### Added
- Instructions on how to install PythonAnywhere. (@hjwp)

### [2016-04-25]
### Added
- Check to confirm that the user has a modern version of Cookiecutter. (@pydanny)

### Removed
- Removed hitch per #529 (@pydanny)

### [2016-04-20]
### Changed
- Default to today's date in cookiecutter.json. (@audreyr)
- Change repo_name to project_slug for clarity. (@audreyr)
- Transform project name to lowercase for slug. (@audreyr)

### [2016-04-19]
### Added
- "Got Questions?" section in our README.rst. Yes, there is now a cookiecutter-django tag on Stack Overflow! (@pydanny)

### Changed
- Update usage instructions with new prompts, minor cleanup (@audreyr)

### [2016-04-18]
### Added
- removing duplication of depends_on in docker-compose.yml (@noisy)

### [2016-04-17]
### Added
- "Built with Cookiecutter Django" badge to generated project README (@audreyr)
- New introductory article (@krzysztofzuraw)

### Changed
- Quote consistency, single quotes everywhere! (@blopker)

### [2016-04-15]
### Changed
- Major project generation cleanup (@jayfk)

### Removed
- Deleting unnecessary .idea dir from MAIN directory (@noisy)

### [2016-04-14]
### Added
- Added typecheck in .pylintrc to fix pylint-django gets "no-member" error (@solvire)

### Changed
- Downgrading python-dateutil to version 2.4.2 because pykwalify==1.5.0 (required by HitchTest) uses a [pinned version of python-dateutil](https://github.com/Grokzen/pykwalify/blob/1.5.0/setup.py#L31) (@noisy)
- Update Pillow version to 3.2.0 (security fix) (@luzfcb)

### [2016-04-12]
### Changed
- celeryworker and celerybeat missing the correct dockerfile (@jayfk)

### [2016-04-08]
### Changed
- Move to named docker volumes (@jayfk)

### [2016-04-07]
### Changed
- Pycharm Support (including debugging in Docker) @noisy
- Set the correct License @epileptic-fish

### [2016-03-23]
### Changed
- Fixed issue on LICENSE file generation (@romanosipenko)
- In install_python_dependencies.sh file, Fixed wrong reference to python3 if use_python2 was set to y (@luzfcb @noisy)

### [2016-03-16]
### Changed
- Set the correct postgres username in dev.yml (@calculuscowboy)

## [2016-03-14]
### Changed
- Enforce `repo_name` as proper python module (@catherinedevlin)

## [2016-03-08]
### Changed
- Docker configuration now uses docker-compose format v2 (@aeikenberry)
- Make sure that STATIC_URL != MEDIA_URL (@cdvv7788)
- fix minor typos in project README (@menzenski)
- Updated docker docs (@jayfk)

### Added
- Added database controls for docker (@jayfk)


## [2016-03-05]
### Changed
- Update version of Django, celery, django-test-plus (@luzfcb)
- Update version of Hitch tests dependencies: jupyter_client (@luzfcb)
- Update 'now' date in cookiecutter.json (@luzfcb)
- Update the usage example in README (@luzfcb)

## [2016-03-01]
### Changed
- Update version of Django, flake8, pyflakes, pytest, factory_boy, ipdb, Werkzeug, gevent (@luzfcb)
- Update version of Hitch tests dependencies: click, hitchserve, hitchsystem, hitchtest, ipython, psutil, python-dateutil(@luzfcb)
- Update Tether (JS) version to 1.2.0 (@luzfcb)

## [2016-02-24]
### Added
- Beginning support for `py.test` (@pydanny)

### Changed
- Fixed missing div closing tag for "container" on user_list.html (@Eraldo)

## [2016-02-18]
### Changed
- The status of the registration (open or closed) is now read from the project environment instead of hardcoded in the common settings file. (@Eraldo)
- Renamed the adapter.py file to adapters.py to match the django naming convention. (@Eraldo)



## [2016-02-15]
### Changed
- In `users` app adapter, fix `is_open_for_signup` missing parameter (@oryx2)
- Fixes and improvements in Hitch tests , see [#485](https://github.com/cookiecutter/cookiecutter-django/pull/485) (@crdoconnor)


## [2016-02-12]
### Changed
- Fixed typo (@yunti)

## [2016-02-07]
### Changed
- In `users` app, use Django 1.9 `LoginRequiredMixin` instead of django-braces implementation (@yunti)
- Update native OS libraries of Hitch Test, because [unixpackage](https://github.com/unixpackage/unixpackage) now supports multiple versions of same Linux distribution (@crdoconnor)
- Update AngularJS version to 1.5.0 (@luzfcb)
- Update version of wheel, Pillow, django_coverage_plugin (@luzfcb)
- Update version of Hitch tests dependencies: decorator, hitchselenium, ipython, ptyprocess, selenium (@luzfcb)
- Provided options for FOSS license choices, or for private efforts, no written license (@pydanny)

## [2016-02-01]
### Changed
- Update version of Django and django-floppyforms (@luzfcb)
- Update version of Hitch tests dependencies: hitchpython and selenium (@luzfcb)

## [2016-01-30]
### Changed
- Update flake8 to 2.5.2 (@luzfcb)

## [2016-01-29]
### Changed
- Update AngularJS version to 1.4.9 (@luzfcb)
- Update jQuery version to 2.2.0 (@luzfcb)
- Update 'now' date in cookiecutter.json (@luzfcb)
- Update version of boto, celery, django_coverage_plugin, django-storages-redux, flake8, gevent, gunicorn, pep8, pytest, tox, Werkzeug (@luzfcb)
- Update version of Hitch tests dependencies: colorama, decorator, hitchpostgres, hitchpython, hitchredis, hitchselenium, hitchserve, hitchsystem, hitchtest, ipython, patool, pickleshare, psutil, python-build, requests, selenium, tblib, traitlets (@luzfcb)


## [2016-01-26]
### Changed
- Fixed NEW_RELIC_APP_NAME environment variable (@jayfk)

## [2016-1-18]
### Added
- Added .dockerignore file (@bogdal)
- Docker tests for travis (@jayfk)

### Changed
- Removed the $-sign from allowed chars to generate the secret key (@jayfk)

## [2016-01-17]
### Added
- Adding a section on third party articles referencing `cookiecutter-django` (@mjheo)

### Changed
- Add celerybeat db to gitignore (@originell)

## [2016-01-16]
### Added
- Adding an explanation for having `django.contrib.sites`. (@pydanny)


## [2016-01-13]
### Changed
- Update setup.py version to 1.9.1 to match Django version. (@Collederas)
- Require Wheel 0.26.0. Needed to install certain packages on CPython 3.5+ like Pillow and psycopg2 (@audreyr)

## [2016-01-09]
### Changed
- Upgraded django-extensions to 1.6.1 as it fixes a [JSONField bug](https://github.com/django-extensions/django-extensions/blob/master/CHANGELOG.md#161) (@burhan)
- Upgraded Pillow to version 3.1.0 ([upstream changelog](https://github.com/python-pillow/Pillow/blob/master/CHANGES.rst#310-2016-01-04)) (@burhan)
- Upgraded django to 1.9.1 to integrate various [bugfixes](https://docs.djangoproject.com/en/1.9/releases/1.9.1/) (@burhan)
- Upgraded django-crispy-forms to 1.6 for [BS4 and django 1.9 compatibility fixes](https://github.com/maraujop/django-crispy-forms/blob/dev/CHANGELOG.md#160-201617) (@burhan)
- Upgraded django-model-utils to 2.4, to enable [support for django 1.9](https://github.com/carljm/django-model-utils/blob/master/CHANGES.rst#24-2015-12-03) (@burhan)

## [2016-01-08]
### Changed
- Fixed redis url on docker (@jayfk)
- Fixed docker on windows (@burhan)

## [2016-01-06]
### Added
- You can now enable or disable user registration using the ACCOUNT_ALLOW_REGISTRATION setting. (@ddiazpinto)

### Changed
- Use Postgres 9.5 on docker (@jayfk)

## [2016-01-04]
### Added
- Add Tether.js because [is needed](http://v4-alpha.getbootstrap.com/components/tooltips/#overview) for proper positioning of Bootstrap tooltips (@EricZaporzan)

### Changed
- Minor fixes in the docker documentation (@jayfk)
- Made @burhan a core committer (@pydanny)

## [2015-12-30]
### Changed
- Fixed a bug where the navbar was not displayed correctly (@jvanbrug)

## [2015-12-21]
### Changed
- Added sentry logger to celery config (@jayfk)

## [2015-12-16]
- Update preview 4xx error pages to accept `exception` argument (@theskumar)

## [2015-12-15]
### Changed
- Fix celery worker app name in Procfile (@stepmr)

## [2015-12-13]
### Changed
- Bumped Django to 1.9 (@areski)
- Support opbeat logging with celery (@stepmr)
- Update runtime.txt with PY2 support (@stepmr)

## [2015-12-12]
### Added
- Celery worker to Heroku procfile (@stepmr)

## [2015-12-11]
### Changed
- Fixed issue #436 - cookiecutter variable name was renamed from `celery_support` to `use_celery` in `tests/engine.py` (@luzfcb @otakucode)
- Updated Heroku runtime.txt for python 3.5.1 (@yunti)

## [2015-12-06]
### Changed
- Reorganization of contributors (@burhan)

## [2015-12-01]
### Changed
- Update documentation to include the installation os dependencies before development requirements (@failsafe86)

## [2015-11-29]
### Changed
- Update version of click and python-build (@luzfcb)

## [2015-11-25]
### Changed
- Update version of psutil, ipython (@luzfcb)
- Update version of gunicorn (@audreyr)
- Remove debugging tools from non-generated part of cookiecutter-django, since those are personal prefs (@audreyr)
- Update version of Django in setup.py (@luzfcb)

## [2015-11-24]
### Changed
- Update version of Django, coverage and click (@luzfcb)
- Fixed configuration for Celery in local.py. (@luzfcb @hackebrot)

## [2015-11-23]
### Changed
- Update AngularJS version to 1.4.8 (@luzfcb)
- Update version of cookiecutter, pytest, tox, whitenoise, django-test-plus, django_coverage_plugin, Werkzeug, hitchserve, tornado, unixpackage (@luzfcb)
- Update 'now' date in cookiecutter.json (@luzfcb)
- `sh` package version pinned to `1.11` (@luzfcb)

## [2015-11-22]
### Changed
- Move div class unquote outside the django if tag (@jvanbrug)
- Changed gevent to `1.1rc1` for python 3 users (@jondelmil / @jayfk)

## [2015-11-20]
### Changed
- Using python 3.5 on Heroku/Travis (@bogdal)
- Fixed typo in README (@tedmiston)

## [2015-11-18]
### Added
- Mailhog as a replacement for Maildump (@keybits)

### Removed
- Maildump because it didn't support Python 3 (@keybits)

## [2015-11-17]
### Added
- initial configuration to support opbeat (@burhan)

### Removed
- Took `*.pyc` out of .gitignore, because it's already covered by `*.py[cod]` (@audreyr)

## [2015-11-16]
### Changed
- Cleanup of main README (@burhan)

## [2015-11-15]
### Added
- Added `UserFactory` for users.User tests (@ad-m)

## [2015-11-12]
### Changed
- Update version of django-allauth (@yunti)
- Added a warning in README.rst: ```repo_name must be a valid Python module``` @cdvv7788

### Removed
- remove ```{% load url from future %}``` in templates - deprecated in django 1.9 (@yunti)

## [2015-11-11]
### Added
- Added django_coverage_plugin to measure Django template coverage (@audreyr)

## [2015-11-09]
### Changed
- Now using py.test for our test suite!! (@hackebrot)
- Python version in travis.yml is now correct for the selected version of Django (@show0k)

## [2015-11-08]
### Changed
- bump django-extensions version (@garrypolley)

## [2015-11-07]
### Added
- newrelic support (@amjith)
- DJANGO_SENTRY_DSN to env.example (@jayfk)

### Changed
- Made `post_gen_hook.set_secret_key()` only changes one CHANGEME!!! at a time. (@pydanny)
- Fixed an error where celery couldn't load the sentry DSN from settings (@jayfk)
- Renamed ADMIN_URL to DJANGO_ADMIN_URL in env.example (@ChrisPappalardo)

## [2015-11-06]
### Added
- \*tests\* to `.coveragerc`, because including it is cheating! (@pydanny)
- Binaryornot to cookiecutter-django's own tests because otherwise Python 3 blows up (@audreyr)

### Changed
- `.travis.yml` configuration to support Python 3.4 and 3.5 (@pydanny)
- `.gitignore` configuration so py.test cache files don't show up in git status.

## [2015-11-05]
### Changed
- Update version of django-extensions (@luzfcb)
- Fix gevent requirement for Python 3 (@mcho421)

## [2015-11-04]
### Changed
- Update version of Django, cookiecutter, celery, coverage, django-mailgun, django-redis, factory_boy, flake8, pytest and pytz (@luzfcb)
- Update AngularJS version to 1.4.7 (@luzfcb)
- Update 'now' date in cookiecutter.json (@luzfcb)

## [2015-10-28]
### Changed
- Update deployment-on-heroku.rst for ADMIN_URL (@yunti)

## [2015-10-27]
### Added
- Added sudo: true to the travis file (@MathijsHoogland)

## [2015-10-25]
### Added
- Move current logging config into production.py since it's not useful locally anyway. Used only if not using Sentry. (@audreyr)
- `setup.py` so we can list it on PyPI and therefore displayed on djangopackages.com as compatible with Python 3. (@pydanny)
- Versioning and tagging policy (@pydanny)
- Fixed flake8 issue (@pydanny)

## [2015-10-24]
### Changed
- Update nav in base template to latest Bootstrap 4 version (@audreyr)
- Replaced ADD with COPY in dockerfiles (@audreyr)
- Simplified development dockerfile (@jayfk)
- Moved the docker postgres volume on the development environment to it's own subfolder (@jayfk)
- Renamed DJANGO_CACHE_URL to REDIS_URL (@jayfk / proposed by @pydanny)

## [2015-10-22]
### Removed
- Remove unnecessary .gitkeep in static/images/ (@audreyr)

## [2015-10-21]
### Changed
- Updated requirements (@theskumar)
### Removed
- editorconfig comment that was just a isort settings link (@pydanny)

## [2015-10-19]
### Changed
- On Windows, don't install psycopg2 locally. Still install it in test/prod which are assumed to be Unix. (@audreyr)

## [2015-10-15]
### Changed
- Made `post_gen_hook` function to change secret keys in files more generic (@pydanny)
- Set cryptographically randomized value to `DJANGO_SECRET_KEY` in `env.example` (@pydanny)

## [2015-10-14]
### Added
- Documention of project options (@audreyr)
### Changed
- Added clarification on building for local or production (@MathijsHoogland)
- Whitespace correction in dev.yml (@MathijsHoogland)

## [2015-10-13]
### Changed
- Requirements update (@theskumar)

## [2015-10-11]
### Changed
- Fixed raven issue on development (#302) (@jazztpt)

## [2015-10-05]
### Changed
- Update version of Django, Pillow, hitchselenium, psutil (@luzfcb)

## [2015-10-04]
### Changed
- Remove stray closing tags and fix navbar margin in in base.html (@hairychris)
- Docker docs to be functional and more understandable (@audreyr)

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
- Fix issue #296 - change login.html to use [get_providers](https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/templatetags/socialaccount.py#L84-L93) templatetag because ``allauth.socialaccount`` context processor now is [deprecated](http://django-allauth.readthedocs.io/en/latest/changelog.html#from-0-21-0) (@luzfcb)

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
