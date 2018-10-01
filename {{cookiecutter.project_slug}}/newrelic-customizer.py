from configparser import SafeConfigParser
from os import getenv
import argparse


def main(options):
    postfix = options.get("postfix", "")

    parser = SafeConfigParser()
    parser.read('newrelic.ini')

    app_name = getenv("NEW_RELIC_APP_NAME", "{{ cookiecutter.project_slug }}")
    if postfix:
        app_name = app_name + "-" + postfix
    parser.set('newrelic', 'app_name', app_name)

    with open('newrelic.ini', 'w') as configfile:
        parser.write(configfile)


if __name__ == '__main__':
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-p", "--postfix", help="posfix for newrelic app name")
    args = vars(arg_p.parse_args())
    main(args)
