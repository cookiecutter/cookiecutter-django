from asyncio import new_event_loop

import pytest
from websockets import connect

from {{cookiecutter.project_slug}}.users.tests.async_server import run_server
from {{cookiecutter.project_slug}}.users.websocket import websocket_application as app


def test_accept_connection():
    async def open_connection(url):
        async with connect(url) as websocket:
            return websocket.open

    with run_server(app) as _url:
        loop = new_event_loop()
        is_open = loop.run_until_complete(open_connection(_url))
        assert is_open
        loop.close()


@pytest.mark.timeout(10)
def test_ping():
    async def open_connection(url):
        async with connect(url) as websocket:
            await websocket.send("ping")
            return await websocket.recv()

    with run_server(app) as _url:
        loop = new_event_loop()
        received_message = loop.run_until_complete(open_connection(_url))
        assert received_message == "pong"
        loop.close()
