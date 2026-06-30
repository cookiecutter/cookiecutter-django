"""Generic FK-context import admin for django-import-export.

Usage example
-------------
Suppose you have a ``Report`` model that belongs to an ``Organisation`` via a
FK.  You want the admin operator to pick the organisation **once** at the top
of the import wizard, and have that value applied to every imported row
automatically — without requiring a column in the CSV file.

1.  Define a resource that inherits the context-injecting mixin::

        # your_app/resources.py
        from import_export import resources
        from {{ cookiecutter.project_slug }}.contrib.import_export.resources import ContextInjectingResource

        class ReportResource(ContextInjectingResource, resources.ModelResource):
            class Meta:
                model = Report

2.  Create an import form with the FK field(s)::

        # your_app/forms.py
        from django import forms
        from .models import Organisation

        class ReportImportForm(forms.Form):
            organisation = forms.ModelChoiceField(
                queryset=Organisation.objects.all(),
                help_text="Applied to every row that omits this column.",
            )

3.  Register the admin::

        # your_app/admin.py
        from django.contrib import admin
        from {{ cookiecutter.project_slug }}.contrib.import_export.admin import FKContextImportExportModelAdmin
        from .models import Report
        from .resources import ReportResource
        from .forms import ReportImportForm

        @admin.register(Report)
        class ReportAdmin(FKContextImportExportModelAdmin):
            resource_classes = [ReportResource]
            import_form_class = ReportImportForm
            # map: import-form field name -> CSV/resource column name
            import_context_fields = {"organisation": "organisation_id"}

When no ``import_context_fields`` are defined the admin behaves identically to
plain ``ImportExportMixin``.
"""

from import_export.admin import ImportExportMixin


class FKContextImportExportModelAdmin(ImportExportMixin):
    """Admin mixin that applies a shared FK value to every imported row.

    Configure :attr:`import_context_fields` as a mapping of
    ``{import_form_field_name: resource_column_name}``.  The value selected
    in the import wizard is forwarded to the resource as a ``context_fields``
    kwarg and then injected into each row by
    :class:`~{{ cookiecutter.project_slug }}.contrib.import_export.resources.ContextInjectingResource`
    before field-level processing runs.

    CSV rows that already contain the column are left untouched, so per-row
    overrides still work.
    """

    #: ``{import-form field name: resource column name}``
    #: Leave empty to get plain ImportExportMixin behaviour.
    import_context_fields: dict[str, str] = {}

    def get_import_data_kwargs(self, request, *args, **kwargs):
        """Collect selected FK values from the import form and forward them."""
        kw = super().get_import_data_kwargs(request, *args, **kwargs)
        form = kwargs.get("form")
        if form and getattr(form, "cleaned_data", None):
            context_fields = {
                col_name: form.cleaned_data[form_field]
                for form_field, col_name in self.import_context_fields.items()
                if form.cleaned_data.get(form_field) is not None
            }
            if context_fields:
                kw["context_fields"] = context_fields
        return kw
