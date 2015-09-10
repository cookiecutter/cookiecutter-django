"""
This code has been adopted from Django's standard crypto functions and
utilities, specifically:
    https://github.com/django/django/blob/master/django/utils/crypto.py
"""
import hashlib
import os
import random
import shutil

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    # import warnings
    # warnings.warn('A secure pseudo-random number generator is not available '
    #               'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False

def get_random_string(
        length=50,
        allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    settings.SECRET_KEY)).encode('utf-8')
            ).digest())
    return ''.join(random.choice(allowed_chars) for i in range(length))

# Get the root project directory
project_directory = os.path.realpath(os.path.curdir)

# Determine the local_setting_file_location
local_setting_file_location = os.path.join(
    project_directory,
    'config/settings/local.py'
)

# Open locals.py
with open(local_setting_file_location) as f:
    local_py = f.read()

# Generate a SECRET_KEY that matches the Django standard
SECRET_KEY = get_random_string()
SECRET_KEY = 'CHANGEME!!!' + SECRET_KEY

# Replace "CHANGEME!!!" with SECRET_KEY
local_py = local_py.replace('CHANGEME!!!', SECRET_KEY)

# Write the results to the locals.py module
with open(local_setting_file_location, 'w') as f:
    f.write(local_py)
