from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.http import HttpResponseBase
    from django.views.generic.base import TemplateResponseMixin
    from django.views.generic.base import View

    from {{ cookiecutter.project_slug }}.typedefs import HtmxHttpRequest

    class _TemplateViewBase(TemplateResponseMixin, View):
        """Typing-only base so mypy knows the methods this mixin overrides."""

else:
    _TemplateViewBase = object


class HtmxTemplateMixin(_TemplateViewBase):
    """Render a partial template for htmx requests and the full template otherwise.

    Set ``htmx_template_name`` on a template-based view. The partial is used only
    when the request carries the ``HX-Request`` header, so every page keeps
    working without htmx. The response gets ``Vary: HX-Request`` because its
    body differs between the two kinds of request.
    """

    htmx_template_name: str | None = None
    request: HtmxHttpRequest

    @method_decorator(vary_on_headers("HX-Request"))
    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponseBase:
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self) -> list[str]:
        if self.htmx_template_name and self.request.htmx:
            return [self.htmx_template_name]
        return super().get_template_names()
