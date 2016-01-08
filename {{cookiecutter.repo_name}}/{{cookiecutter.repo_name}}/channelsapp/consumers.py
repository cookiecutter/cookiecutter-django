"""
This is an example for a channels app using the getting started guide at
https://channels.readthedocs.org/en/latest/getting-started.html
"""
from channels import Group

# Connected to websocket.connect and websocket.keepalive
def ws_add(message):
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    Group("chat").send(message.content)

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
