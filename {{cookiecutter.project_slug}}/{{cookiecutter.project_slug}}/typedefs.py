"""Project-wide type definitions.

Views, mixins and API endpoints import their request types from here so the
whole project shares one vocabulary instead of narrowing ``request.user`` by
hand in every method.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpRequest
{%- if cookiecutter.rest_api == 'DRF' %}
from rest_framework.request import Request
{%- endif %}

if TYPE_CHECKING:
    from django_htmx.middleware import HtmxDetails

    from {{ cookiecutter.project_slug }}.users.models import User


class AuthenticatedHttpRequest(HttpRequest):
    """Request whose ``user`` is known to be logged in.

    Declare ``request: AuthenticatedHttpRequest`` on a view guarded by
    ``LoginRequiredMixin`` or ``login_required`` and ``request.user`` is a
    ``User`` in every method of that view.
    """

    user: User


class HtmxHttpRequest(HttpRequest):
    """Request carrying the ``htmx`` attribute added by ``HtmxMiddleware``."""

    htmx: HtmxDetails


class AuthenticatedHtmxRequest(AuthenticatedHttpRequest, HtmxHttpRequest):
    """Request that is both authenticated and annotated by ``HtmxMiddleware``."""
{%- if cookiecutter.rest_api == 'DRF' %}


class AuthenticatedApiRequest(Request):
    """Django REST framework request whose ``user`` is known to be logged in.

    Declare ``request: AuthenticatedApiRequest`` on views and viewsets that run
    under the ``IsAuthenticated`` permission class.
    """

    user: User
{%- endif %}
