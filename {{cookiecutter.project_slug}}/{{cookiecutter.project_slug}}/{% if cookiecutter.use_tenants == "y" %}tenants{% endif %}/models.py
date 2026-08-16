from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase


class Tenant(TenantBase):
    """Project tenant metadata stored in the public schema."""

    name = models.CharField(_("Tenant Name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")

    def __str__(self) -> str:
        return self.name


class Domain(DomainMixin):
    """Tenant domain mapping for host-based tenant routing."""

    class Meta:
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")
