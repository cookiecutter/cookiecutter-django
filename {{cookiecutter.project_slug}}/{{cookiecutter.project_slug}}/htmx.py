from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import cast

from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers

if TYPE_CHECKING:
    from django.http import HttpResponseBase
    from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    """Request annotated with the ``htmx`` attribute added by ``HtmxMiddleware``."""

    htmx: HtmxDetails


class HtmxTemplateMixin:
    """Render a partial template for htmx requests and the full template otherwise.

    Set ``htmx_template_name`` on a template-based view. The partial is used only
    when the request carries the ``HX-Request`` header, so every page keeps
    working without htmx. The response gets ``Vary: HX-Request`` because its
    body differs between the two kinds of request.
    """

    htmx_template_name: str | None = None
    request: HttpRequest

    @method_decorator(vary_on_headers("HX-Request"))
    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponseBase:
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]

    def get_template_names(self) -> list[str]:
        request = cast("HtmxHttpRequest", self.request)
        if self.htmx_template_name and request.htmx:
            return [self.htmx_template_name]
        return super().get_template_names()  # type: ignore[misc]
