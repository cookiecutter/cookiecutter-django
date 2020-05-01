"""
Refer to Uvicorn's tests to know how to write your own.
https://github.com/encode/uvicorn/blob/master/tests/protocols/test_websocket.py

"""
from asyncio import new_event_loop
from websockets import connect

from {{ cookiecutter.project_slug }}.users.tests.async_server import run_server


def test_accept_connection():
    """
    If you want to communicate over HTTP, add live_server fixture
    """
    async def open_connection(url):
        async with connect(url) as websocket:
            return websocket.open

    with run_server() as url:
        loop = new_event_loop()
        is_open = loop.run_until_complete(open_connection(url))
        assert is_open
        loop.close()


def test_ping():
    async def ping(url):
        async with connect(url) as websocket:
            await websocket.send("ping")
            return await websocket.recv()

    with run_server() as url:
        loop = new_event_loop()
        received_message = loop.run_until_complete(ping(url))
        assert received_message == "pong"
        loop.close()
