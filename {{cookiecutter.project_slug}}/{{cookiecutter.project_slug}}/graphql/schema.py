# -*- coding: utf-8 -*-
import sys

from django.conf import settings

from graphene import Schema

# NOTE: Conversions need to happen before importing from queries/mutations
from . import conversions  # NOQA
from . import mutation, query


# NOTE: As Graphene schema gets larger, it needs more room to run the recursive graphql queries
# See: https://github.com/graphql-python/graphene/issues/663
sys.setrecursionlimit(settings.GRAPHENE_RECURSION_LIMIT)


schema = Schema(query=query.Query, mutation=mutation.Mutation)
