Channels
========

Cookiecutter-django comes with (experimental) channels support. A basic skeleton of a Django
project with channels is generated automatically for you if you choose to `use_channels` during
project setup.

.. note:: If you are using docker, a websocket server and the worker processes are started
automatically for you. Just replace 127.0.0.1 with the IP of your docker-machine you are running.

There's a basic app called `channelsapp` created automatically for you. It uses the routes from
`conf/routes.py`. The app is based on the `channels getting started guide
<https://channels.readthedocs.org/en/latest/getting-started.html>`_.

To see if your websocket server is started, go to http://127.0.0.1:9000/. You should see a greeting
message from autobahn.

Now, to get started, just open a browser and put the following into the JavaScript console
to test your new code::

    socket = new WebSocket("ws://127.0.0.1:9000");
    socket.onmessage = function(e) {
        alert(e.data);
    }
    socket.send("hello world");


You should see an alert come back immediately saying "hello world" - your
message has round-tripped through the server and come back to trigger the alert.
