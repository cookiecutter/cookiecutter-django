# -*- coding: utf-8 -*-
from graphene import Field, ObjectType
from graphene_django.debug import DjangoDebug


class Query(ObjectType):
    debug = Field(DjangoDebug, name='__debug')
