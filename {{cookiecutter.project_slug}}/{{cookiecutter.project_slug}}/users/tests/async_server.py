import asyncio
import functools
import threading
import time
from contextlib import contextmanager

from uvicorn.config import Config
from uvicorn.main import ServerState
from uvicorn.protocols.http.h11_impl import H11Protocol
from uvicorn.protocols.websockets.websockets_impl import WebSocketProtocol


def run_loop(loop):
    loop.run_forever()
    loop.close()


@contextmanager
def run_server(app, path="/"):
    asyncio.set_event_loop(None)
    loop = asyncio.new_event_loop()
    config = Config(app=app, ws=WebSocketProtocol)
    server_state = ServerState()
    protocol = functools.partial(H11Protocol, config=config, server_state=server_state)
    create_server_task = loop.create_server(protocol, host="127.0.0.1")
    server = loop.run_until_complete(create_server_task)  # type: ignore 
    port = server.sockets[0].getsockname()[1]
    url = "ws://127.0.0.1:{port}{path}".format(port=port, path=path)
    try:
        # Run the event loop in a new thread.
        thread = threading.Thread(target=run_loop, args=[loop])
        thread.start()
        # Return the contextmanager state.
        yield url
    finally:
        # Close the loop from our main thread.
        while server_state.tasks:
            time.sleep(0.01)
        loop.call_soon_threadsafe(loop.stop)
        thread.join()
