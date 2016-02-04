"""
This is an example for a channels routing config using the getting started guide at
https://channels.readthedocs.org/en/latest/getting-started.html
"""
channel_routing = {
    "websocket.connect": "{{cookiecutter.repo_name}}.channelsapp.consumers.ws_add",
    "websocket.keepalive": "{{cookiecutter.repo_name}}.channelsapp.consumers.ws_add",
    "websocket.receive": "{{cookiecutter.repo_name}}.channelsapp.consumers.ws_message",
    "websocket.disconnect": "{{cookiecutter.repo_name}}.channelsapp.consumers.ws_disconnect",
}
