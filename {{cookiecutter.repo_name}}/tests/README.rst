Hitch tests
===========

Note: This has been tested on up to date versions Debian, Ubuntu, Arch and
Mac OS X (Mavericks).

To initialize and run the hitch tests in your project, enter this (tests) directory and
run the following command::

  $ curl -sSL https://hitchtest.com/init.sh > init.sh ; chmod +x init.sh ; ./init.sh

Note: if you are running Mac OS X you will need to install firefox as well.
You can do this while it is running.

This should download install all the necessary packages and run the stub test.
It will take about 10 or 15 minutes to set up.

Once it is ready, you should see a browser window and an interactive IPython prompt::

    IPython 4.0.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]:

For more documentation on hitch, see: https://hitchtest.readthedocs.org/en/latest/api/index.html

If anything goes wrong during the set up process, please raise an issue at
https://github.com/hitchtest/hitch/issues
