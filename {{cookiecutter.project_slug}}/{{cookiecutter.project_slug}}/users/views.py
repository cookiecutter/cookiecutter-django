from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ModelForm
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from {{ cookiecutter.project_slug }}.htmx import HtmxTemplateMixin
from {{ cookiecutter.project_slug }}.users.models import User

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from {{ cookiecutter.project_slug }}.typedefs import AuthenticatedHtmxRequest
    from {{ cookiecutter.project_slug }}.typedefs import AuthenticatedHttpRequest


class UserDetailView(LoginRequiredMixin, HtmxTemplateMixin, DetailView[User]):
    model = User
    request: AuthenticatedHtmxRequest
    htmx_template_name = "users/partials/user_detail.html"
    {%- if cookiecutter.username_type == "email" %}
    slug_field = "id"
    slug_url_kwarg = "id"
    {%- else %}
    slug_field = "username"
    slug_url_kwarg = "username"
    {%- endif %}


user_detail_view = UserDetailView.as_view()


class UserUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin[ModelForm[User]],
    HtmxTemplateMixin,
    UpdateView[User, ModelForm[User]],
):
    model = User
    request: AuthenticatedHtmxRequest
    fields = ["name"]
    htmx_template_name = "users/partials/user_form.html"
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet[User] | None = None) -> User:
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
    request: AuthenticatedHttpRequest

    def get_redirect_url(self) -> str:
        {%- if cookiecutter.username_type == "email" %}
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})
        {%- else %}
        return reverse("users:detail", kwargs={"username": self.request.user.username})
        {%- endif %}


user_redirect_view = UserRedirectView.as_view()
