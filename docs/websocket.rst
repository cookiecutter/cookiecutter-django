.. _websocket:

=========
Websocket
=========

You can enable web sockets if you select ``use_async`` option when creating a project. That indicates whether the project can use web sockets with Uvicorn + Gunicorn.

Usage
-----

JavaScript example: ::

    > ws = new WebSocket('ws://localhost:8000/') // or 'wss://<mydomain.com>/' in prod
    WebSocket {url: "ws://localhost:8000/", readyState: 0, bufferedAmount: 0, onopen: null, onerror: null, …}
    > ws.onmessage = event => console.log(event.data)
    event => console.log(event.data)
    > ws.send("ping")
    undefined
    pong!


If you don't use Traefik, you might have to configure your reverse proxy accordingly (example with Nginx_).

.. _Nginx: https://www.nginx.com/blog/websocket-nginx/
