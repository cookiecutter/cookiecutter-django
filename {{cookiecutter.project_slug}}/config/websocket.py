from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable
    from collections.abc import Callable
    from collections.abc import Mapping
    from typing import Any

# The loose ASGI shapes Django's own handler accepts.
type ASGIScope = dict[str, Any]
type ASGIReceive = Callable[[], Awaitable[Mapping[str, Any]]]
type ASGISend = Callable[[Mapping[str, Any]], Awaitable[None]]


async def websocket_application(
    scope: ASGIScope,
    receive: ASGIReceive,
    send: ASGISend,
) -> None:
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive":
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong!"})
