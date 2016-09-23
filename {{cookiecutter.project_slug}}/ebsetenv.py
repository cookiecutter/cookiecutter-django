"""Converts a .env file to Elastic Beanstalk environment variables"""

from sys import exit
from subprocess import check_call

try:
    import dotenv
except ImportError:
    print("Please install the 'dotenv' library: 'pip install dotenv'")
    exit()

def main():
    command = ['eb', 'setenv']
    failures = []
    for key, value in dotenv.Dotenv('.env').items():
        if key.startswith('POSTGRES'):
            continue
        if value:
            command.append("{}={}".format(key, value))
        else:
            failures.append(key)
    if failures:
        for failure in failures:
            print("{} requires a value".format(failure))
    else:
        print(' '.join(command))
        check_call(command)


if __name__ == '__main__':
    main()
