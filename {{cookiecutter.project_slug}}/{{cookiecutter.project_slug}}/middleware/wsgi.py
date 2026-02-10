import warnings
from wsgiref.util import request_uri

class WSGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"
        await self._run_wsgi_app(scope, receive, send)

    async def _run_wsgi_app(self, scope, receive, send):
        # Implementation of WSGI middleware logic
        pass

warnings.warn(
    "The WSGI middleware is deprecated and will be removed in a future release.\n    Consider using `a2wsgi` instead.",
    DeprecationWarning,
    stacklevel=2,
)