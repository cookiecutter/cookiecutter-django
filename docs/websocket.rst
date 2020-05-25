.. _websocket:

=========
Websocket
=========

You can enable web sockets if you select ``use_async`` option when creating a project. That indicates whether the project should use web sockets with Uvicorn + Gunicorn.

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

If you are using nGinx instead of Traefik, you should add these lines to nGinx config: ::

    location /websocket/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

Source: https://www.nginx.com/blog/websocket-nginx/
