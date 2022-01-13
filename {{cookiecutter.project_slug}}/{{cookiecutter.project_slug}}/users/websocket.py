async def websocket_application(scope, receive, send):
    event = await receive()
    if event["type"] == "websocket.connect":
        # TODO Add authentication by reading scope
        #  and getting sessionid from cookie
        await send({"type": "websocket.accept"})
    else:
        await send({"type": "websocket.close"})
        return

    while True:
        event = await receive()
        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive":
            if event["text"] == "ping":
                await send({"type": "websocket.send", "text": "pong"})
