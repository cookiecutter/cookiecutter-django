"""Converts a .env file to Elastic Beanstalk environment variables"""

import os
from sys import exit
from subprocess import check_call

try:
    import dotenv
except ImportError:
    print("Please install the 'dotenv' library: 'pip install dotenv'")
    exit()

def main():
    if not os.path.exists('.env'):
        print('ERROR!! .env file is missing!')
        print("Please copy 'env.example' to '.env' and add appropriate values")
        exit()
    command = ['eb', 'setenv']
    failures = []
    for key, value in dotenv.Dotenv('.env').items():
        if key.startswith('POSTGRES'):
            print('Skipping POSTGRES values - Amazon RDS provides these')
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
