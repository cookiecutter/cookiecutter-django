class ContextInjectingResource:
    """Mixin that injects shared FK context values into every imported row.

    Works together with :class:`~.admin.FKContextImportExportModelAdmin`.
    Values passed via the ``context_fields`` kwarg are written into each data
    row *before* field-level processing, so CSV/XLSX files do not need a
    dedicated column for those fields.

    Usage
    -----
    Combine this mixin with ``resources.ModelResource``::

        from import_export import resources
        from {{ cookiecutter.project_slug }}.contrib.import_export.resources import ContextInjectingResource

        class ReportResource(ContextInjectingResource, resources.ModelResource):
            class Meta:
                model = Report

    The mixin will silently skip columns that are already present in the row,
    so it is safe to include the FK column in the file when you want per-row
    control and still use the global default for rows that omit it.
    """

    def before_import_row(self, row, row_number=None, **kwargs):
        """Inject context-supplied values into the current row when absent."""
        super().before_import_row(row, row_number=row_number, **kwargs)
        for col_name, value in kwargs.get("context_fields", {}).items():
            if not row.get(col_name):
                row[col_name] = value
