# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models import FileField
from django.forms import Field

from django_filters import Filter
from graphene import Float, Int, JSONString, List, String
from graphene_django.converter import convert_django_field
from graphene_django.forms.converter import convert_form_field


# NOTE: This needs to be done before importing from queries
# SEE: https://github.com/graphql-python/graphene-django/issues/18
@convert_django_field.register(ArrayField)
def convert_array_to_list(field, registry=None):
    return List(of_type=String, description=field.help_text, required=not field.null)


@convert_django_field.register(JSONField)
def convert_jsonb_to_string(field, registry=None):
    return JSONString(description=field.help_text, required=not field.null)


@convert_django_field.register(FileField)
def convert_file_to_string(field, registry=None):
    return String(description=field.help_text, required=not field.null)


def generate_list_filter_class(inner_type):
    """
    Returns a Filter class that will resolve into a List(`inner_type`) graphene
    type.

    This allows us to do things like use `__in` filters that accept graphene
    lists instead of a comma delimited value string that's interpolated into
    a list by django_filters.BaseCSVFilter (which is used to define
    django_filters.BaseInFilter)
    """

    form_field = type(
        "List{}FormField".format(inner_type.__name__),
        (Field,),
        {},
    )
    filter_class = type(
        "{}ListFilter".format(inner_type.__name__),
        (Filter,),
        {
            "field_class": form_field,
            "__doc__": (
                "{0}ListFilter is a small extension of a raw django_filters.Filter "
                "that allows us to express graphql List({0}) arguments using FilterSets."
                "Note that the given values are passed directly into queryset filters."
            ).format(inner_type.__name__),
        },
    )
    convert_form_field.register(form_field)(
        lambda x: List(inner_type, required=x.required)
    )

    return filter_class


FloatListFilter = generate_list_filter_class(Float)
IntListFilter = generate_list_filter_class(Int)
StringListFilter = generate_list_filter_class(String)
