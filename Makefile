up:
	@docker-compose -f local.yml up

build:
	@docker-compose -f local.yml up --force-recreate --build

manage:
	@docker-compose -f local.yml run --rm django python ./manage.py $(filter-out $@,$(MAKECMDGOALS)) --settings=config.settings.local

# https://stackoverflow.com/a/6273809/1826109
%:
	@:

