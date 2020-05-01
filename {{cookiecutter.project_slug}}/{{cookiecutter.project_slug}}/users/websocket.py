async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            # TODO Add authentication using DRF-SimpleJWT or other token methods
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive":
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong"})
